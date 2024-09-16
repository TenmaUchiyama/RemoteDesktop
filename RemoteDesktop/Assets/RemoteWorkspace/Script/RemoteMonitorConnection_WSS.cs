using UnityEngine;
using UnityEngine.UI;
using System;
using System.Collections.Concurrent;
using WebSocketSharp;
using Unity.VisualScripting;
using UnityEngine.XR.Interaction.Toolkit.UI;

public class RemoteMonitorConnection_WSS : MonoBehaviour  
{
    private string endpoint=""; 

    private WebSocket webSocket;
    private GameObject monitorObject;

    private RawImage rawImage;
    private Texture2D texture;
    private ConcurrentQueue<byte[]> imageQueue;
    private bool sizeSet = false;

    public RemoteMonitorConnection_WSS (string endpoint, GameObject parentObject )
    {
        this.endpoint = endpoint;
        imageQueue = new ConcurrentQueue<byte[]>();
        Initialize(parentObject);
    }

    private void Initialize(GameObject parentObject)
    {
        // WebSocket接続の作成
        string url = $"ws://192.168.10.102:8765/{this.endpoint}";
        webSocket = new WebSocket(url);

        // イベントハンドラの設定
        webSocket.OnOpen += (sender, e) => Debug.Log($"WebSocket connected to {url}");
        webSocket.OnMessage += OnMessage;
        webSocket.OnError += OnError;
        webSocket.OnClose += OnClose;

        webSocket.ConnectAsync();

        // Monitorのオブジェクト追加
        monitorObject = new GameObject();
        monitorObject.name = "Monitor";
        monitorObject.transform.SetParent(parentObject.transform, false);

        // キャンバスの追加
        Canvas monitorCanvas = monitorObject.AddComponent<Canvas>();
        monitorCanvas.AddComponent<CanvasScaler>();
        monitorCanvas.renderMode = RenderMode.WorldSpace;
        monitorCanvas.worldCamera = Camera.main;
        monitorCanvas.AddComponent<TrackedDeviceGraphicRaycaster>();

        // RawImageの追加
        rawImage = monitorCanvas.gameObject.AddComponent<RawImage>();
        rawImage.rectTransform.anchorMin = new Vector2(0, 0);
        rawImage.rectTransform.anchorMax = new Vector2(1, 1);
        rawImage.rectTransform.anchoredPosition = Vector2.zero;
        rawImage.rectTransform.sizeDelta = Vector2.zero;

        // 初期化
        RectTransform rectTransform = monitorObject.GetComponent<RectTransform>();
        rectTransform.sizeDelta = new Vector2(200, 200); // 必要に応じてサイズを調整

        Vector3 objPos = rectTransform.localPosition;
        objPos.y += 1.23f;
        rectTransform.localPosition = objPos;

        // テクスチャの初期化
        texture = new Texture2D(1, 1);
        rawImage.texture = texture;
    }

    private void OnMessage(object sender, MessageEventArgs e)
    {
        if (e.IsBinary && e.RawData.Length > 0)
        {
            imageQueue.Enqueue(e.RawData);
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

    public void Update()
    {
        while (imageQueue.TryDequeue(out byte[] imageData))
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
