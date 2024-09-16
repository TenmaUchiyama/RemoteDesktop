using UnityEngine;
using UnityEngine.UI;
using System;
using System.Net.WebSockets;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Concurrent;
using PimDeWitte.UnityMainThreadDispatcher;
using UnityEngine.Events;




public class RemoteMonitorConnection
{
    private string endpoint=""; 

    private ClientWebSocket webSocket;

    private RawImage rawImage;
    private Texture2D texture;
    private CancellationTokenSource cancellationTokenSource;
    private ConcurrentQueue<byte[]> imageQueue;
    private bool sizeSet = false;

    public OnCloseConnectionUnityEvent OnCloseConnection = new OnCloseConnectionUnityEvent();

    [System.Serializable]
public class OnCloseConnectionUnityEvent : UnityEvent<OnCloseConnectionArgs>
{
}
    
    [System.Serializable]
    public class OnCloseConnectionArgs
    {
        public string endpoint;
    }
    public RemoteMonitorConnection (string endpoint, RawImage rawImage )
    {      
        this.endpoint = endpoint;
        imageQueue = new ConcurrentQueue<byte[]>();

        this.rawImage = rawImage;
        texture = new Texture2D(2, 2);
        texture.anisoLevel = 10; 
        rawImage.texture = texture;
        ConectionInitialize();
    }

    private void ConectionInitialize()
    {
        // Create WebSocket connection
        string url = $"ws://localhost:8765/{this.endpoint}";
        webSocket = new ClientWebSocket();
        cancellationTokenSource = new CancellationTokenSource();
        ConnectAsync(url);
    }

    private async void ConnectAsync(string url)
    {
        try
        {
            Uri uri = new Uri(url);
            await webSocket.ConnectAsync(uri, cancellationTokenSource.Token);
            Debug.Log($"WebSocket connected to {url}");
            await ReceiveLoopAsync();
        }
        catch (Exception ex)
        {
            Debug.LogError($"WebSocket connection error for endpoint {this.endpoint}: {ex.Message}");
            Close();  
       
        }
    }

    private async Task ReceiveLoopAsync()
    {
    var buffer = new byte[1024 * 1024]; 
    try
    {
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
        Close();  
       
    }
    catch (Exception ex)
    {
        Debug.LogError($"Unexpected error during WebSocket receive loop: {ex.Message}");
        Close();   
    }
   
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
                Close();
            }
        }
    }
}




private void SetRectTransformSize()
{
    if (texture != null && rawImage != null)
    {
        int width = texture.width;
        int height = texture.height;

        RectTransform rectTransform = rawImage.gameObject.GetComponent<RectTransform>();
        if (rectTransform != null)
        {
            float fixedHeight = 3.2f; 
            float aspectRatio = (float)width / height;
            rectTransform.sizeDelta = new Vector2(fixedHeight * aspectRatio, fixedHeight);
           
          
        }
    }
}


   public void Close()
{
    if (webSocket != null)
    {
        try
        {
            webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closed by client", CancellationToken.None).Wait();
        }
        catch (Exception ex)
        {
            Debug.LogError($"Error closing WebSocket: {ex.Message}");
        }
        cancellationTokenSource.Cancel();
        webSocket.Dispose();
        webSocket = null;
    }

   UnityMainThreadDispatcher.Instance().Enqueue(() =>
    {
        OnCloseConnection.Invoke(new OnCloseConnectionArgs { endpoint = this.endpoint });
    });
}

}
