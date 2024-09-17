using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using Unity.VisualScripting;
using UnityEditor.Rendering;
using UnityEditor.XR.Interaction.Toolkit.Utilities;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem.Interactions;
using UnityEngine.UI;

public class MonitorInput : MonoBehaviour , IPointerMoveHandler, IPointerEnterHandler  , IPointerExitHandler
{
   private RemoteMonitorManager remoteMonitorManager;

   private MonitorInputConnection inputConnection;


   private bool isFrameGrabbed = false;
   
   public Image cursorImage; 

   private string monitor_id;

    RectTransform targetRectTransform;
    
    private string monitor_type;

    

    private void Start() {
        targetRectTransform = GetComponent<RectTransform>();


        ControllerInput.Instance.onTriggerPressed.AddListener(() => {
           
            if(!this.inputConnection) return;
            Task.Run(async () => {await this.inputConnection.SendPressBtn(true);}); 
        });

        ControllerInput.Instance.onTriggerReleased.AddListener(() => {
            if(!this.inputConnection) return;
         
            Task.Run(async () => {await this.inputConnection.SendPressBtn(false);}); 
        });


        ControllerInput.Instance.onGripperPressed.AddListener(() => {
            if(!this.inputConnection) return;
            Task.Run(async () => {await this.inputConnection.SendRightClick();}); 
        });




        ControllerInput.Instance.onFlickLeftUp.AddListener(() => {
            Task.Run(async () => {await this.inputConnection.SendLeftScroll(true);}); 
        });


        ControllerInput.Instance.onFlickLeftDown.AddListener(() => {
            Task.Run(async () => {await this.inputConnection.SendLeftScroll(false);}); 
        });


    }

   public void SetProcessInput(string monitor_id , string monitor_type, MonitorInputConnection inputConnection, RemoteMonitorManager remoteMonitorManager)
   {
        
        
        
       this.inputConnection = inputConnection;
        this.monitor_id = monitor_id;
        this.monitor_type = monitor_type;
        this.remoteMonitorManager = remoteMonitorManager;
   }




   public void DisplayEvent(string theEvent)
   {
    
   }

    public void OnPointerEnter(PointerEventData eventData)
{
    
    cursorImage.gameObject.SetActive(true);
    this.inputConnection.SetIsOnMonitor(true, this.monitor_id, this.monitor_type);
}


    public void OnPointerExit(PointerEventData eventData)
{
    

    cursorImage.gameObject.SetActive(false);
    this.inputConnection.SetIsOnMonitor(false, "", "");
}


 
    public void OnPointerClick(PointerEventData eventData)
    {
       if(!this.inputConnection) return;
        Task.Run(async () => {await this.inputConnection.SendPressBtn(false);}); 
    }

    public void OnBeginDrag(PointerEventData eventData)
    {
        throw new System.NotImplementedException();
    }

    public void OnDrag(PointerEventData eventData)
    {
        throw new System.NotImplementedException();
    }


    public void SetIsFrameGrabbed(bool isFrameGrabbed)
    {
        this.isFrameGrabbed = isFrameGrabbed;
    }

    void IPointerMoveHandler.OnPointerMove(PointerEventData eventData)
    {
    
       
        Vector3 worldPosition = eventData.pointerCurrentRaycast.worldPosition;

       
        Vector3 localPosition = targetRectTransform.InverseTransformPoint(worldPosition);

      
        Vector2 rectSize = targetRectTransform.rect.size;

   
        float relativeX = (localPosition.x / rectSize.x) + 0.5f; 
        float relativeY = (localPosition.y / rectSize.y) + 1f; 

        
        
        cursorImage.rectTransform.localPosition = localPosition;

        if(!this.inputConnection) return; 
        Task.Run(async () => {await this.inputConnection.SetCursorPosition(this.monitor_id, this.monitor_type, new Vector2(relativeX, relativeY));});

    

  
}




    private void Update() {
        if(!ControllerInput.Instance) return; 
        if(ControllerInput.Instance.IsRightTouchpadTouchedOnce)
        {
            float delta = ControllerInput.Instance.DeltaValueR;
            Task.Run(async () => {await this.inputConnection.SendScroll(delta);});
        }
        if(isFrameGrabbed)
        {   
          
            
            float getScrollValue = ControllerInput.Instance.DeltaValueR; 



            float originalWidth = this.targetRectTransform.sizeDelta.x;
            float originalHeight = this.targetRectTransform.sizeDelta.y;
            float aspectRatio = originalWidth / originalHeight;
            float newWidth = originalWidth + getScrollValue;    
            float newHeight = newWidth / aspectRatio;
            targetRectTransform.sizeDelta =  new Vector2(newWidth, newHeight);
        }
    }
    public  void CloseWindow()
    {
        this.remoteMonitorManager.RemoveConnection(this.monitor_id);
    }
}