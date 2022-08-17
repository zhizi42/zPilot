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
#include <chrono>
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
static float TestLoopCallback(float inElapsedSinceLastCall, float inElapsedTimeSinceLastFlightLoop, int inCounter, void* inRefcon);

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
static XPLMDataRef gPlaneVX;
static XPLMDataRef gPlaneVY;
static XPLMDataRef gPlaneVZ;
static XPLMDataRef gPlaneAX;
static XPLMDataRef gPlaneAY;
static XPLMDataRef gPlaneAZ;
static XPLMDataRef gPlaneP;
static XPLMDataRef gPlaneQ;
static XPLMDataRef gPlaneR;
static XPLMDataRef gPlanePD;
static XPLMDataRef gPlaneQD;
static XPLMDataRef gPlaneRD;

PLUGIN_API int XPluginStart(	char *		outName,
								char *		outSig,
								char *		outDesc)
{
	strcpy(outName, "zConnect");
	strcpy(outSig, "com.zhizi42.zconnect");
	strcpy(outDesc, "A plugin that connect zPilot server.");

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
	gPlaneVX = XPLMFindDataRef("sim/flightmodel/position/local_vx");
	gPlaneVY = XPLMFindDataRef("sim/flightmodel/position/local_vy");
	gPlaneVZ = XPLMFindDataRef("sim/flightmodel/position/local_vz");
	gPlaneAX = XPLMFindDataRef("sim/flightmodel/position/local_ax");
	gPlaneAY = XPLMFindDataRef("sim/flightmodel/position/local_ay");
	gPlaneAZ = XPLMFindDataRef("sim/flightmodel/position/local_az");
	gPlaneP = XPLMFindDataRef("sim/flightmodel/position/P");
	gPlaneQ = XPLMFindDataRef("sim/flightmodel/position/Q");
	gPlaneR = XPLMFindDataRef("sim/flightmodel/position/R");
	gPlanePD = XPLMFindDataRef("sim/flightmodel/position/P_dot");
	gPlaneQD = XPLMFindDataRef("sim/flightmodel/position/Q_dot");
	gPlaneRD = XPLMFindDataRef("sim/flightmodel/position/R_dot");

	XPLMRegisterFlightLoopCallback(
		MyFlightLoopCallback,	/* Callback */
		1.0,					/* Interval */
		NULL);
	XPLMRegisterFlightLoopCallback(SendDataLoopCallback, 1.0, NULL);
	XPLMRegisterFlightLoopCallback(TestLoopCallback, 1.0, NULL);
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
std::map<std::string, std::map<std::string, double>> otherPilotData;

float	MyFlightLoopCallback(
                                   float                inElapsedSinceLastCall,    
                                   float                inElapsedTimeSinceLastFlightLoop,    
                                   int                  inCounter,    
                                   void *               inRefcon)
{
	static auto startTime = std::chrono::steady_clock::now();
	int t = std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now() - startTime).count();
	double frameTime = t / 1000000000.0;
	startTime = std::chrono::steady_clock::now();

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


		otherPilotData[cs]["vx"] += otherPilotData[cs]["ax"] * frameTime;
		otherPilotData[cs]["vy"] += otherPilotData[cs]["ay"] * frameTime;
		otherPilotData[cs]["vz"] += otherPilotData[cs]["az"] * frameTime;
		otherPilotData[cs]["x"] += otherPilotData[cs]["vx"] * frameTime;
		otherPilotData[cs]["y"] += otherPilotData[cs]["vy"] * frameTime;
		otherPilotData[cs]["z"] += otherPilotData[cs]["vz"] * frameTime;
		otherPilotData[cs]["p"] += otherPilotData[cs]["pd"] * frameTime;
		otherPilotData[cs]["q"] += otherPilotData[cs]["qd"] * frameTime;
		otherPilotData[cs]["r"] += otherPilotData[cs]["rd"] * frameTime;
		otherPilotData[cs]["the"] += otherPilotData[cs]["q"] * frameTime;
		otherPilotData[cs]["phi"] += otherPilotData[cs]["p"] * frameTime;
		otherPilotData[cs]["psi"] += otherPilotData[cs]["r"] * frameTime;


		XPLMDrawInfo_t *pos = new XPLMDrawInfo_t();
		pos->structSize = 24;
		pos->x = otherPilotData[cs]["x"];
		pos->y = otherPilotData[cs]["y"];
		pos->z = otherPilotData[cs]["z"];
		pos->pitch = otherPilotData[cs]["the"];
		pos->heading = otherPilotData[cs]["psi"];
		pos->roll = otherPilotData[cs]["phi"];
		
		char x[20];
		char y[20];
		char z[20];
		sprintf(x, "%f", otherPilotData[cs]["vx"]);
		sprintf(y, "%f", otherPilotData[cs]["vy"]);
		sprintf(z, "%f", otherPilotData[cs]["vz"]);
		XPLMDebugString("cs:");
		XPLMDebugString(cs.c_str());
		XPLMDebugString("\n");
		XPLMDebugString("vx:");
		XPLMDebugString(x);
		XPLMDebugString("\n");
		XPLMDebugString("vy:");
		XPLMDebugString(y);
		XPLMDebugString("\n");
		XPLMDebugString("vz:");
		XPLMDebugString(z);
		XPLMDebugString("\n");/**/

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
			std::string cmd = jsonRecv["cmd"].as_string();
			if (cmd == "pd")
			{
				std::map<std::string, double> m;
				double lat = std::stod(jsonRecv["lat"].as_string());
				double lon = std::stod(jsonRecv["lon"].as_string());
				double alt = std::stod(jsonRecv["alt"].as_string());
				double x, y, z;
				XPLMWorldToLocal(lat, lon, alt, &x, &y, &z);
				m["x"] = x;
				m["y"] = y;
				m["z"] = z;
				m["lat"] = lat;
				m["lon"] = lon;
				m["alt"] = alt;
				m["the"] = std::stod(jsonRecv["the"].as_string());
				m["phi"] = std::stod(jsonRecv["phi"].as_string());
				m["psi"] = std::stod(jsonRecv["psi"].as_string());
				m["gs"] = std::stod(jsonRecv["gs"].as_string());
				m["vx"] = std::stod(jsonRecv["vx"].as_string());
				m["vy"] = std::stod(jsonRecv["vy"].as_string());
				m["vz"] = std::stod(jsonRecv["vz"].as_string());
				m["ax"] = std::stod(jsonRecv["ax"].as_string());
				m["ay"] = std::stod(jsonRecv["ay"].as_string());
				m["az"] = std::stod(jsonRecv["az"].as_string());
				m["p"] = std::stod(jsonRecv["p"].as_string());
				m["q"] = std::stod(jsonRecv["q"].as_string());
				m["r"] = std::stod(jsonRecv["r"].as_string());
				m["p_dot"] = std::stod(jsonRecv["p_dot"].as_string());
				m["q_dot"] = std::stod(jsonRecv["q_dot"].as_string());
				m["r_dot"] = std::stod(jsonRecv["r_dot"].as_string());
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
	char charVX[10], charVY[10], charVZ[10], charAX[10], charAY[10], charAZ[10];
	char charP[10], charQ[10], charR[12], charPD[10], charQD[10], charRD[10];
	sprintf(charLat, "%f", XPLMGetDataf(gPlaneLat));
	sprintf(charLon, "%f", XPLMGetDataf(gPlaneLon));
	sprintf(charAlt, "%f", XPLMGetDataf(gPlaneEle));
	sprintf(charThe, "%f", XPLMGetDataf(gPlaneTheta));
	sprintf(charPhi, "%f", XPLMGetDataf(gPlanePhi));
	sprintf(charPsi, "%f", XPLMGetDataf(gPlanePsi));
	sprintf(charGs, "%f", XPLMGetDataf(gPlaneGs));
	sprintf(charVX, "%f", XPLMGetDataf(gPlaneVX));
	sprintf(charVY, "%f", XPLMGetDataf(gPlaneVY));
	sprintf(charVZ, "%f", XPLMGetDataf(gPlaneVZ));
	sprintf(charAX, "%f", XPLMGetDataf(gPlaneAX));
	sprintf(charAY, "%f", XPLMGetDataf(gPlaneAY));
	sprintf(charAZ, "%f", XPLMGetDataf(gPlaneAZ));
	sprintf(charP, "%f", XPLMGetDataf(gPlaneP));
	sprintf(charQ, "%f", XPLMGetDataf(gPlaneQ));
	sprintf(charR, "%f", XPLMGetDataf(gPlaneR));
	sprintf(charPD, "%f", XPLMGetDataf(gPlanePD));
	sprintf(charQD, "%f", XPLMGetDataf(gPlaneQD));
	sprintf(charRD, "%f", XPLMGetDataf(gPlaneRD));

	json jsonMsg;
	jsonMsg["lat"] = charLat;//纬度
	jsonMsg["lon"] = charLon;//经度
	jsonMsg["alt"] = charAlt;//高度
	jsonMsg["the"] = charThe;//俯仰
	jsonMsg["phi"] = charPhi;//滚动
	jsonMsg["psi"] = charPsi;//航向
	jsonMsg["gs"] = charGs;//地速
	jsonMsg["vx"] = charVX;//x速度
	jsonMsg["vy"] = charVY;//y速度
	jsonMsg["vz"] = charVZ;//z速度
	jsonMsg["ax"] = charAX;//x加速度
	jsonMsg["ay"] = charAY;//y加速度
	jsonMsg["az"] = charAZ;//z加速度
	jsonMsg["p"] = charP;//滚动速度
	jsonMsg["q"] = charQ;//俯仰速度
	jsonMsg["r"] = charR;//航向速度
	jsonMsg["p_dot"] = charPD;//滚动加速度
	jsonMsg["q_dot"] = charQD;//俯仰加速度
	jsonMsg["r_dot"] = charRD;//航向加速度

	char* charMsg = (char*)jsonMsg.dump().c_str();
	int l = sendMsg(charMsg);
	if (l <= 0)
	{
		isConnect = false;
		return -1;
	}

	return 1;
}

float TestLoopCallback(float inElapsedSinceLastCall, float inElapsedTimeSinceLastFlightLoop, int inCounter, void* inRefcon)
{
	return -1;
}