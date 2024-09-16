using System;
using System.Net.WebSockets;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.UI;
using PimDeWitte.UnityMainThreadDispatcher;

public class ScreenCapture : MonoBehaviour
{
    private ClientWebSocket webSocket;
    public RawImage rawImage;
    private Texture2D texture;
    private Thread receiveThread;

    private async void Start()
    {
        // RawImage コンポーネントがセットされているか確認
        if (rawImage == null)
        {
            Debug.LogError("RawImageコンポーネントが見つかりません。");
            return;
        }

        // テクスチャを初期化
        texture = new Texture2D(1920, 1080);
        rawImage.texture = texture;

        // WebSocket 接続を確立
        webSocket = new ClientWebSocket();
        await ConnectWebSocket();

        // 受信スレッドを開始
        receiveThread = new Thread(async () => await ReceiveMessages());
        receiveThread.Start();
    }

    private async Task ConnectWebSocket()
    {
        try
        {
            // WebSocket サーバーに接続
            Uri serverUri = new Uri("ws://192.168.10.102:8765/1");
            await webSocket.ConnectAsync(serverUri, CancellationToken.None);
            Debug.Log("WebSocket接続が開かれました。");
        }
        catch (Exception ex)
        {
            Debug.LogError("WebSocketエラー: " + ex.Message);
        }
    }



    private async Task ReceiveMessages()
    {
        var buffer = new byte[1024 * 1024]; // 1MB のバッファ
        try
        {
            while (webSocket.State == WebSocketState.Open)
            {
                // メッセージを受信
                WebSocketReceiveResult result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);

                // データが受信された場合のみ処理
                if (result.Count > 0)
                {
                    byte[] jpegBytes = new byte[result.Count];
                    Array.Copy(buffer, jpegBytes, result.Count);

                    // メインスレッドでテクスチャにデータを反映
                    UnityMainThreadDispatcher.Instance().Enqueue(() =>
                    {
                        texture.LoadImage(jpegBytes);
                        texture.Apply();
                    });
                }
            }
        }
        catch (Exception ex)
        {
            Debug.LogError("WebSocket受信エラー: " + ex.Message);
        }
    }

    private void OnDestroy()
    {
        if (receiveThread != null && receiveThread.IsAlive)
        {
            receiveThread.Abort();
        }

        if (webSocket != null)
        {
            webSocket.Dispose();
        }
    }
}
