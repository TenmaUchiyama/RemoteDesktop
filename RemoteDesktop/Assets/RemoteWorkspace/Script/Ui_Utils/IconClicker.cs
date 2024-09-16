using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.XR.Interaction.Toolkit.Interactors;

[System.Serializable]
public class MonitorIcon
{
    public string name;  
    public string type; 
    public Transform monitorInitPosition; 
}

public class IconClicker : MonoBehaviour
{
    
    public RemoteMonitorManager remoteMonitorManager;
    public List<MonitorIcon> monitorIcons = new List<MonitorIcon>();


    private void Start() {
        remoteMonitorManager.AddConnection("1", "monitor", remoteMonitorManager.gameObject.transform);
    }

    
    public MonitorIcon GetMonitorIconByName(string iconName)
    {
        foreach (MonitorIcon icon in monitorIcons)
        {
            if (icon.name == iconName)
            {
                return icon;
            }
        }

     
        
        return null;
    }

    
    public void StartMonitor(string iconName)
    {
        MonitorIcon icon = GetMonitorIconByName(iconName);

        if (icon != null)
        {
           
            Transform iconTransform = icon.monitorInitPosition;
            string iconType = icon.type;

            remoteMonitorManager.AddConnection(iconName, iconType, iconTransform);
        }
      
    }
}