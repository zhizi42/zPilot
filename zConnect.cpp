// Downloaded from https://developer.x-plane.com/code-sample/drawaircraft/



/*
	DrawAircraft example
	Written by Sandy Barbour - 11/02/2003

	Modified by Sandy Barbour - 07/12/2009
	Combined source files and fixed a few bugs.
	
	This examples Draws 7 AI aircraft around the user aicraft.
	It also uses an Aircraft class to simplify things.

	This is a very simple example intended to show how to use the AI datarefs.
	In a production plugin Aircraft Aquisition and Release would have to be handled.
	Also loading the approriate aircraft model would also have to be done.
	This example may be updated to do that at a later time.

	NOTE
	Set the aircraft number to 8 in the XPlane Aircraft & Situations settings screen.
*/

#include <string.h>
#include <math.h>
#include <thread>
#include <map>
#include "Connect.h"
#include "jsonxx/json.hpp"
#include "XPLMPlanes.h"
#include "XPLMDataAccess.h"
#include "XPLMProcessing.h"
#include "XPLMGraphics.h"
#include "XPLMInstance.h"
#include "XPLMScenery.h"
#include "XPLMUtilities.h"

using namespace jsonxx;

static float	MyFlightLoopCallback(
                                   float                inElapsedSinceLastCall,    
                                   float                inElapsedTimeSinceLastFlightLoop,    
                                   int                  inCounter,    
                                   void *               inRefcon);

static float SendDataLoopCallback(float inElapsedSinceLastCall, float inElapsedTimeSinceLastFlightLoop, int inCounter, void* inRefcon);

void RecvDataLoop();

/*static XPLMDataRef gPlaneX;
static XPLMDataRef gPlaneY;
static XPLMDataRef gPlaneZ;*/
static XPLMDataRef gPlaneLat;
static XPLMDataRef gPlaneLon;
static XPLMDataRef gPlaneEle;
static XPLMDataRef gPlaneTheta;
static XPLMDataRef gPlanePhi;
static XPLMDataRef gPlanePsi;
static XPLMDataRef gPlaneGs;

PLUGIN_API int XPluginStart(	char *		outName,
								char *		outSig,
								char *		outDesc)
{
	strcpy(outName, "zConnect");
	strcpy(outSig, "com.zhizi42.zconnect");
	strcpy(outDesc, "A plugin that connect fsd server.");

	/*gPlaneX = XPLMFindDataRef("sim/flightmodel/position/local_x");
	gPlaneY = XPLMFindDataRef("sim/flightmodel/position/local_y");
	gPlaneZ = XPLMFindDataRef("sim/flightmodel/position/local_z");*/
	gPlaneLat = XPLMFindDataRef("sim/flightmodel/position/latitude");
	gPlaneLon = XPLMFindDataRef("sim/flightmodel/position/longitude");
	gPlaneEle = XPLMFindDataRef("sim/flightmodel/position/elevation");
	gPlaneTheta = XPLMFindDataRef("sim/flightmodel/position/true_theta");
	gPlanePhi = XPLMFindDataRef("sim/flightmodel/position/true_phi");
	gPlanePsi = XPLMFindDataRef("sim/flightmodel/position/true_psi");
	gPlaneGs = XPLMFindDataRef("sim/flightmodel/position/groundspeed");

	XPLMRegisterFlightLoopCallback(
		MyFlightLoopCallback,	/* Callback */
		1.0,					/* Interval */
		NULL);
	XPLMRegisterFlightLoopCallback(SendDataLoopCallback, 1.0, NULL);

	return 1;
}


PLUGIN_API void	XPluginStop(void)
{
	XPLMUnregisterFlightLoopCallback(MyFlightLoopCallback, NULL);
}

PLUGIN_API void XPluginDisable(void)
{
}

PLUGIN_API int XPluginEnable(void)
{
	return 1;
}

PLUGIN_API void XPluginReceiveMessage(	XPLMPluginID	inFromWho,
										int				inMessage,
										void *			inParam)
{
}


XPLMObjectRef B738obj = XPLMLoadObject("Resources\\plugins\\X-IvAp Resources\\CSL\\B738\\B738ai.obj");
std::map<std::string, XPLMInstanceRef> planeInstanceMap;
std::map<std::string, std::map<std::string, std::string>> otherPilotData;

float	MyFlightLoopCallback(
                                   float                inElapsedSinceLastCall,    
                                   float                inElapsedTimeSinceLastFlightLoop,    
                                   int                  inCounter,    
                                   void *               inRefcon)
{
	for (auto it = otherPilotData.begin(); it != otherPilotData.end(); it++)
	{
		std::string cs = it->first;
		int i = planeInstanceMap.count(cs);
		if (i == 0)
		{
			const char* nullArray[] = { NULL };
			XPLMInstanceRef B738ins = XPLMCreateInstance(B738obj, nullArray);
			planeInstanceMap[cs] = B738ins;
		}

		double planeLat = std::stod(it->second["lat"]);
		double planeLon = std::stod(it->second["lon"]);
		double planeAlt = std::stod(it->second["alt"]);
		double planeX, planeY, planeZ;
	    XPLMWorldToLocal(planeLat, planeLon, planeAlt, &planeX, &planeY, &planeZ);
		
		XPLMDrawInfo_t *pos = new XPLMDrawInfo_t();
		pos->structSize = 24;
		pos->x = planeX;
		pos->y = planeY;
		pos->z = planeZ;
		pos->pitch = 0;
		pos->heading = 0;
		pos->roll = 0;
		
		/*char lat[10];
		char lon[10];
		char alt[10];
		sprintf(lat, "%f", planeLat);
		sprintf(lon, "%f", planeLon);
		sprintf(alt, "%f", planeAlt);
		XPLMDebugString("cs:");
		XPLMDebugString(cs.c_str());
		XPLMDebugString("\n");
		XPLMDebugString("lat:");
		XPLMDebugString(lat);
		XPLMDebugString("\n");
		XPLMDebugString("lon:");
		XPLMDebugString(lon);
		XPLMDebugString("\n");
		XPLMDebugString("alt:");
		XPLMDebugString(alt);
		XPLMDebugString("\n");*/

		XPLMInstanceRef ref = planeInstanceMap[cs];
		XPLMInstanceSetPosition(ref, pos, NULL);
	}

	return -1;
}

bool isConnect = false;
void ic() {
	if (initConnect())
	{
		isConnect = true;
		std::thread recvData(RecvDataLoop);
		recvData.detach();
	};
}

void RecvDataLoop() {
	while (true)
	{
		char* charRecv;
		try
		{
			charRecv = recvMsg();
		}
		catch (const std::exception&e)
		{
			isConnect = false;
			break;
		}
		if (charRecv == "")
		{
			isConnect = false;
			break;
		}
		try
		{
			json jsonRecv = json::parse(charRecv);
			std::string action = jsonRecv["action"].as_string();
			if (action == "pilot_data")
			{
				std::map<std::string, std::string> m;
				m["lat"] = jsonRecv["lat"].as_string();
				m["lon"] = jsonRecv["lon"].as_string();
				m["alt"] = jsonRecv["alt"].as_string();
				m["gs"] = jsonRecv["gs"].as_string();
				otherPilotData[jsonRecv["cs"].as_string()] = m;
			}
		}
		catch (const std::exception&e)
		{
			XPLMDebugString(e.what());
		}
		
	}
}

float SendDataLoopCallback(float inElapsedSinceLastCall, float inElapsedTimeSinceLastFlightLoop, int inCounter, void* inRefcon) {
	if (!isConnect)
	{
        std::thread t(ic);
		t.detach();
		return 2;
	}

	char charLat[10], charLon[10], charAlt[12], charThe[10], charPhi[10], charPsi[10], charGs[11];
	sprintf(charLat, "%f", XPLMGetDataf(gPlaneLat));
	sprintf(charLon, "%f", XPLMGetDataf(gPlaneLon));
	sprintf(charAlt, "%f", XPLMGetDataf(gPlaneEle));
	sprintf(charThe, "%f", XPLMGetDataf(gPlaneTheta));
	sprintf(charPhi, "%f", XPLMGetDataf(gPlanePhi));
	sprintf(charPsi, "%f", XPLMGetDataf(gPlanePsi));
	sprintf(charGs, "%f", XPLMGetDataf(gPlaneGs));

	json jsonMsg;
	jsonMsg["lat"] = charLat;//纬度
	jsonMsg["lon"] = charLon;//经度
	jsonMsg["alt"] = charAlt;//高度
	jsonMsg["the"] = charThe;//俯仰
	jsonMsg["phi"] = charPhi;//翻转
	jsonMsg["psi"] = charPsi;//航向
	jsonMsg["gs"] = charGs;//地速

	char* charMsg = (char*)jsonMsg.dump().data();
	int l = sendMsg(charMsg);
	if (l <= 0)
	{
		isConnect = false;
		return -1;
	}

	return 1;
}