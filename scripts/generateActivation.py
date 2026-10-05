import os

DEST_DIR = 'activationScripts'

GODOT_CODE = """
using Godot;
using System;
using System.Text;
using System.Text.Json;


public class MoCapReceiver : Node3D
{
    private PackedPeerUdp _udp = new PackedPeerUdp();
    private int _port = 5005;

    public class Joint
    {
        public float x {get; set; }
        public float y {get; set;}
        public float z {get; set; }
    }

    public class MoCapData
    {
        public Joint ombro_d {get; set; } public Joint ombro_e {get; set; }
        public Joint cotovelo_d {get; set; } public Joint cotovelo_e {get; set; }
        public Joint pulso_d {get; set; } public Joint pulso_e {get; set; }
        public Joint joelho_d {get; set; } public Joint joelho_e {get; set; }
        public Joint tornozelo_d {get; set; } public Joint tornozelo_e {get; set; }
    }

    public MoCapData latestData {get; private set; }

    public override void _Ready()
    {
        Error err = _udp.Listen(_port);
        if (err != Error.Ok)
        {
            GD.PrintErr("Failed to listen on UDP port: ", err);
        }
        else
        {
            GD.Print("Listening for MoCap data on UDP port ", _port);
        }
    }

    public override void _Process(double delta)
    {
        while (_udp.GetAvailablePacketCount() > 0)
        {
            byte[] packet = _udp.GetPacket();
            string jsonString = Encoding.UTF8.GetString(packet);

            try
            {
                latestData = JsonSerializer.Deserialize<MoCapData>(jsonString);
            }
            catch (Exception e)
            {
                GD.PrintErr("Failed to deserialize JSON: ", e.Message);
            }
        }
    }
}

"""

UNITY_CODE = """"
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class MoCapReceiver : MonoBehaviour
{
    private Thread receiveThread;
    private UdpClient client;
    private int port = 5005; 

    [System.Serializable]
    public class Joint
    {
        public float x;
        public float y;
        public float z;
    }

    [System.Serializable]
    public class MoCapData
    {
        public Joint ombro_d; public Joint ombro_e;
        public Joint cotovelo_d; public Joint cotovelo_e;
        public Joint pulso_d; public Joint pulso_e;
        public Joint joelho_d; public Joint joelho_e;
        public Joint tornozelo_d; public Joint tornozelo_e;
    }

    public MoCapData latestData;

    void Start()
    {
        receiveThread = new Thread(new ThreadStart(ReceiveData)) {IsBackground = true};
        receiveThread.Start();
    }

    void ReceiveData()
    {
        client = new UdpClient(port);
        while (true)
        {
            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, port);
                byte[] data = client.Receive(ref anyIP);
                string json = Encoding.UTF8.GetString(data);
                latestData = JsonUtility.FromJson<MoCapData>(json);
            }
            catch (System.Exception err)
            {
                Debug.LogError(err.ToString());
                break;
            }
        }
    }

    void OnApplicationQuit()
    {
        if (receiveThread != null)
        {
            receiveThread.Abort();
        }
        if (client != null)
        {
            client.Close();
        }
    }
}
"""

UNREAL_H = """"
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Networking.h"
#include "Sockets.h"
#include "Common/UdpSocketReceiver.h"
#include "Dom/JsonObject.h"
#include "HAL/CriticalSection.h"
#include "MoCapReceiver.generated.h"

UCLASS()
class YOURPROJECT_API AMoCapReceiver : public AActor
{
    GENERATED_BODY()
    
public:    
    AMoCapReceiver();
    virtual void Tick(float DeltaTime) override;

protected:
    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

private:
    FSocket* ListenSocket;
    FUdpSocketReceiver* UDPReceiver;
    void Recv(const FArrayReaderPtr& ArrayReaderPtr, const FIPv4Endpoint& EndPt);
    TSharedPtr<FJsonObject> LatestMoCapData;
    FCriticalSection DataCriticalSection;
};
"""

UNREAL_CPP = """"
#include "MoCapReceiver.h"
#include "Common/UdpSocketBuilder.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"


AMoCapReceiver::AMoCapReceiver()
{
    PrimaryActorTick.bCanEverTick = true;
    ListenSocket = nullptr;
    UDPReceiver = nullptr;
}

void AMoCapReceiver::BeginPlay()
{
    Super::BeginPlay();
    FIPv4Address Addr;
    FIPv4Address::Parse(TEXT("127.0.0.1"), Addr);
    FIPv4Endpoint Endpoint(Addr, 5005);

    ListenSocket = FUdpSocketBuilder(TEXT("MoCapSocket"))
        .AsNonBlocking()
        .AsReusable()
        .BoundToEndpoint(Endpoint)
        .WithReceiveBufferSize(2 * 1024 * 1024);

    if (ListenSocket) 
    {
        FTimespan ThreadWaitTime = FTimespan::FromMilliseconds(100);
        UDPReceiver = new FUdpSocketReceiver(ListenSocket, ThreadWaitTime, TEXT("UdpReceiverThread"));
        UDPReceiver->OnDataReceived().BindUObject(this, &AMoCapReceiver::Recv);
        UDPReceiver->Start();
    }
}

void AMoCapReceiver::Recv(const FArrayReaderPtr& ArrayReaderPtr, const FIPv4Endpoint& EndPt)
{
   if(!ArrayReaderPtr.isValid() || ArrayReaderPtr -> Num() == 0) return;
   FString DataString = FString(UTF8_TO_TCHAR(reinterpret_cast<const char*>(ArrayReaderPtr -> GetData())));
   int32 JsonEndIndex;
   if(DataString.FindLastChar(TEXT('}'), JsonEndIndex)) DataString = DataString.Left(JsonEndIndex + 1);

   TSharedPtr<FJsonObject> JsonObject;
   TSharedRef<TJsonObject<>> Reader = TJsonReaderFactory<>::Create(DataString);

   if(FJsonSerializer::Deserializer(Reader, JsonObject) && JsonObject.isValid())
   {
    FScopeLock Lock(&DataCriticalSection);
    LatestMoCapData = JsonObject;
   }
}

void AMoCapReceiver::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    FScopeLock Lock(&DataCriticalSection);

    if (LatestMoCapData.IsValid())
    {
        TSharedPtr<FJsonObject> OmbroD = LatestMoCapData->GetObjectField(TEXT("ombro_d"));
        if (OmbroD.IsValid())
        {
            float X = OmbroD->GetNumberField(TEXT("x"));
            float Y = OmbroD->GetNumberField(TEXT("y"));
            float Z = OmbroD->GetNumberField(TEXT("z"));
        }
    }
}

void AMoCapReceiver::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    Super::EndPlay(EndPlayReason);
    if (UDPReceiver) {
        UDPReceiver->Stop();
        delete UDPReceiver;
        UDPReceiver = nullptr;
    }
    if (ListenSocket) {
        ListenSocket->Close();
        ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(ListenSocket);
    }
}
"""

def generateTarget(target):
    os.makedirs(DEST_DIR, exist_ok = True)
    target = target.lower().strip()

    if target == "godot":
        path = os.path.join(DEST_DIR, "MoCapReceiver.cs")
        with open(path, "w", encoding="utf-8") as f:
            f.write(GODOT_CODE)
        print(f"\n[+] Arquivo gerado com sucesso: {path}")

    elif target == "unity":
        path = os.path.join(DEST_DIR, "MoCapReceiver.cs")
        with open(path, "w", encoding="utf-8") as f:
            f.write(UNITY_CODE)
        print(f"\n[+] Arquivo gerado com sucesso: {path}")

    elif target == "unreal":
        path_h = os.path.join(DEST_DIR, "MoCapReceiver.h")
        path_cpp = os.path.join(DEST_DIR, "MoCapReceiver.cpp")

        with open(path_h, "w", encoding="utf-8") as f:
            f.write(UNREAL_H)
        with open(path_cpp, "w", encoding="utf-8") as f:
            f.write(UNREAL_CPP)
        print(f"\n[+] Arquivo gerado com sucesso:\n - {path_h} \n - {path_cpp}")
    
