using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.WebSockets;
using System.Threading;
using System.Collections.Concurrent;
using System;
using System.Threading.Tasks;
using Newtonsoft.Json;

public class MonitorInputConnection : MonoBehaviour
{
    ClientWebSocket webSocket;
    CancellationTokenSource cancellationTokenSource;
    ConcurrentQueue<byte[]> imageQueue;
    

    private bool isOnMonitor = false; 


    private string currentFocusMonitorId = ""; 

    int maxRetryAttempts = 5; 
    int retryDelay = 2000; 

    void Start()
    {
        ConnectionInitialize();
    }

    private void ConnectionInitialize()
    {
        string uri = $"ws://localhost:8765/monitor_input";
        cancellationTokenSource = new CancellationTokenSource();
        webSocket = new ClientWebSocket();
        ConnectWithRetryAsync(uri);
    }

    public void SetIsOnMonitor(bool isOnMonitor, string monitor_id, string monitor_type)
    {
        this.isOnMonitor = isOnMonitor;
        this.currentFocusMonitorId = monitor_id;
    } 

    async private void ConnectWithRetryAsync(string uri)
    {
        int retryCount = 0;
        while (retryCount < maxRetryAttempts)
        {
            try
            {
                Uri URI = new Uri(uri);
                await webSocket.ConnectAsync(URI, cancellationTokenSource.Token);
                Debug.Log($"WebSocket connected to {URI}");
                await ReceiveLoopAsync();
                break; 
            }
            catch (System.Exception ex)
            {
                retryCount++;
                Debug.LogError($"WebSocket connection error: {ex.Message}. Retrying in {retryDelay / 1000} seconds... ({retryCount}/{maxRetryAttempts})");

                if (retryCount >= maxRetryAttempts)
                {
                    Debug.LogError("Max retry attempts reached. Failed to connect.");
                    break;
                }

              
            }
        }
    }

    async private Task ReceiveLoopAsync()
    {
        try
        {
            byte[] buffer = new byte[1024];

            while (webSocket.State == WebSocketState.Open)
            {
                var result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), cancellationTokenSource.Token);

                if (result.MessageType == WebSocketMessageType.Close)
                {
                    // Server initiated close, properly close the connection
                    await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, CancellationToken.None);
                    Debug.Log("WebSocket connection closed by server.");
                    break;
                }

                if (result.Count > 0)
                {
                    byte[] receivedData = new byte[result.Count];
                    Array.Copy(buffer, receivedData, result.Count);
                    imageQueue.Enqueue(receivedData);
                }
            }
        }
        catch (WebSocketException ex)
        {
            Debug.LogError($"WebSocket exception: {ex.Message}");
           
        }
        catch (Exception ex)
        {
            Debug.LogError($"Unexpected error during WebSocket receive loop: {ex.Message}");
           
        }
    }

    private async Task ReconnectAsync()
    {
        Debug.Log("Attempting to reconnect...");
        await Task.Delay(retryDelay); 
        ConnectionInitialize(); 
    }

    public async Task SendClick()
    {
        string message = JsonConvert.SerializeObject(
            new {
                type = "click",
            }
        );
        await SendData(message);
    }


    public async Task SendDoubleClick()
    {
        string message = JsonConvert.SerializeObject(
            new {
                type = "double_click",
            }
        );
        await SendData(message);
    }


    public async Task SendRightClick() 
    {
    string message = JsonConvert.SerializeObject(
            new {
                type = "right_click",
              
            }
        );
    
        await SendData(message);
    }

    public async Task SendLeftScroll(bool isFlickUp )
    {
        

    
           string message = JsonConvert.SerializeObject(
                new {
                    type = isFlickUp ? "go_forward": "go_back",
                    monitor_id = this.currentFocusMonitorId

                }
            );
       




        await SendData(message);

    }

    public async Task SendPressBtn(bool value)
    {
        string message = JsonConvert.SerializeObject(
            new {
                type = "mouse_press",
                value = value
            }
        );
      
        await SendData(message);
    }


    public async Task SendScroll(float value)
    {
        string message = JsonConvert.SerializeObject(
            new {
                type = "scroll",
                value = value
            }
        );
        await SendData(message);
    }
    public async Task SetCursorPosition(string monitor_id, string monitor_type, Vector2 position)
    {
        string message = JsonConvert.SerializeObject(
            new {
                type = "cursor",
                monitor_type = monitor_type,
                monitor_id = monitor_id,
                position = new {
                    x = position.x,
                    y = position.y
                }
            }
        );
        await SendData(message);
    }




    private async Task SendData(string message)
    {

      
        if(message == "") return;
        if(!isOnMonitor) return;
        if (webSocket.State == WebSocketState.Open)
        {
            byte[] buffer = System.Text.Encoding.UTF8.GetBytes(message);
            await webSocket.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, cancellationTokenSource.Token);
        }
    }

    public void Close()
    {
        if (webSocket != null)
        {
            cancellationTokenSource.Cancel();
            webSocket.Dispose();
            webSocket = null;
        }
    }


    
}
