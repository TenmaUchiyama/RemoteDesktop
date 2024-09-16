using System.Collections.Generic;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.UI;
using static RemoteMonitorConnection;

public class RemoteMonitorManager : MonoBehaviour
{
    public GameObject monitorParents; // Assign in the Inspector
    public GameObject monitorPrefab;
    public MonitorInputConnection inputConnection;
    private string monitor_type = "";

    private Dictionary<string, RemoteMonitorConnection> connections = new Dictionary<string, RemoteMonitorConnection>();
    private Dictionary<string, GameObject> monitorObjects = new Dictionary<string, GameObject>();

    void Update()
    {
        // Update all active connections
        foreach (var connection in connections.Values)
        {
            connection.Update();
        }
    }

    public void AddConnection(string endpoint, string monitor_type, Transform monitorInitPosition)
    { Debug.Log("Connected");
        if (!connections.ContainsKey(endpoint))
    {

        this.monitor_type = monitor_type;
        Debug.Log("Endpoint: " + endpoint);

        var instantiateWindow = Instantiate(monitorPrefab, monitorParents.transform);  
        instantiateWindow.name = "Monitor_" + endpoint;
        instantiateWindow.transform.position = monitorInitPosition.position;
        instantiateWindow.transform.rotation = monitorInitPosition.rotation;
        instantiateWindow.SetActive(true);

        GameObject monitorImageObject = null; 
        foreach (Transform child in instantiateWindow.transform) // Changed here
        {
            if (child.CompareTag("MonitorImage"))
            {
                monitorImageObject = child.gameObject;
                break; // Exit loop once found
            }
        }

        if (!monitorImageObject)
        {
            Debug.LogError("MonitorImage object not found in the instantiated prefab.");
            return; 
        }

        RawImage monitorImage = monitorImageObject.GetComponent<RawImage>();
        if (monitorImage == null)
        {
            Debug.LogError("RawImage component not found on MonitorImage object.");
            return;
        }

        monitorImageObject.GetComponent<MonitorInput>().SetProcessInput(endpoint , this.monitor_type, inputConnection, this);

        var connection = new RemoteMonitorConnection(endpoint, monitorImage);
        Debug.Log("Connection: " + connection);
        connections.Add(endpoint, connection);
        monitorObjects.Add(endpoint, instantiateWindow);

         connection.OnCloseConnection.AddListener((OnCloseConnectionArgs args) => {
        
             if (monitorObjects.TryGetValue(endpoint, out GameObject monitorObject))
            {
                Destroy(monitorObject);
                monitorObjects.Remove(endpoint);
            }
        }); 
    }
    else
        {
            Debug.LogWarning($"Connection to endpoint {endpoint} already exists.");
        }
    }

    public void RemoveConnection(string endpoint)
{
    if (connections.TryGetValue(endpoint, out RemoteMonitorConnection connection))
    {
        connection.Close();
        connections.Remove(endpoint);

       
    }
    else
    {
        Debug.LogWarning($"Connection to endpoint {endpoint} does not exist.");
    }
}

    

    private void OnDestroy()
    {
      
        foreach (var connection in connections.Values)
        {
            connection.Close();
        }

        foreach(var monitorObject in monitorObjects.Values)
        {
            Destroy(monitorObject);
        }
        connections.Clear();
        monitorObjects.Clear();
        
    }




  
}
