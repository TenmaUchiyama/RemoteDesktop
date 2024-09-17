using UnityEngine;
using UnityEngine.UI;
using System;
using System.Collections.Concurrent;
using WebSocketSharp;
using Unity.VisualScripting;
using UnityEngine.XR.Interaction.Toolkit.UI;
using PimDeWitte.UnityMainThreadDispatcher;

public class RemoteMonitorConnection_WSS : MonoBehaviour  
{
    private string endpoint=""; 

    private WebSocket webSocket;
    private GameObject monitorObject;

    private RawImage rawImage;
    private Texture2D texture;
    private bool sizeSet = false;

    public RemoteMonitorConnection_WSS (string endpoint, RawImage rawImage )
    {
        this.endpoint = endpoint;
       

        this.rawImage = rawImage;
        texture = new Texture2D(2, 2);
        texture.anisoLevel = 10; 
        rawImage.texture = texture;
        ConectionInitialize();
    }

    private void ConectionInitialize()
    {
        // WebSocket接続の作成
        string url = $"ws://localhost:8765/{this.endpoint}";
        webSocket = new WebSocket(url);

        // イベントハンドラの設定
        webSocket.OnOpen += (sender, e) => Debug.Log($"WebSocket connected to {url}");
        webSocket.OnMessage += OnMessage;
        webSocket.OnError += OnError;
        webSocket.OnClose += OnClose;

        webSocket.ConnectAsync();

      
    }

    private void OnMessage(object sender, MessageEventArgs e)
    {
        if (e.IsBinary && e.RawData.Length > 0)
        {
            UnityMainThreadDispatcher.Instance().Enqueue(() => LoadImage(e.RawData));
        }
    }

    private void OnError(object sender, ErrorEventArgs e)
    {
        Debug.LogError($"WebSocket error for endpoint {this.endpoint}: {e.Message}");
    }

    private void OnClose(object sender, CloseEventArgs e)
    {
        Debug.Log($"WebSocket connection closed for endpoint {this.endpoint}: {e.Reason}");
    }

    public void LoadImage(byte[] imageData)
    {
        
            if (imageData != null && imageData.Length > 0)
            {
                try
                {
                    if (texture.LoadImage(imageData))
                    {
                        texture.Apply();

                        if (!sizeSet)
                        {
                            SetRectTransformSize();
                            sizeSet = true;
                        }
                    }
                }
                catch (Exception ex)
                {
                    Debug.LogError($"Error loading image data for endpoint {this.endpoint}: {ex.Message}");
                }
            }
        
    }

    private void SetRectTransformSize()
    {
        if (texture != null && monitorObject != null)
        {
            int width = texture.width;
            int height = texture.height;

            RectTransform rectTransform = monitorObject.GetComponent<RectTransform>();
            if (rectTransform != null)
            {
                float fixedHeight = 2.5f; 
                float aspectRatio = (float)width / height;
                rectTransform.sizeDelta = new Vector2(fixedHeight * aspectRatio, fixedHeight);
            }
        }
    }

    public void Close()
    {
        if (webSocket != null)
        {
            webSocket.Close();
            webSocket = null;
        }
       
    }
}
