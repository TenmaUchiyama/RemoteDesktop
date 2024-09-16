using System;
using System.Collections;
using System.Collections.Generic;

using System.Threading;
using Unity.VisualScripting;
using UnityEditor.Rendering;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.InputSystem;

public class ControllerInput : MonoBehaviour
{


    public static ControllerInput Instance { get; private set; }


    private void Awake() {
        if(Instance == null){
            Instance = this;
        }
    }


    XRIDefaultInputActions xrControllerAction;


    public MonitorInputConnection monitorInputConnection;



    public UnityEvent onTriggerPressed;
    public UnityEvent onTriggerReleased;
    public UnityEvent onGripperPressed;
    public UnityEvent onTouchpadTouched;
    public UnityEvent onTouchpadReleased;
    public UnityEvent onTouchpadTouchedLeft;
    public UnityEvent onTouchpadReleasedLeft;
    public UnityEvent onFlickLeftUp; 
    public UnityEvent onFlickLeftDown;



    

    private bool isRightTouchpadTouchedOnce = false;
    private bool isLeftTouchpadTouchedOnce = false; 

    
    private float previousScrollYRight = 0f;
    private float previousScrollYLeft = 0f;
    private float deltaValueR = 0f;
    

    public bool IsRightTouchpadTouchedOnce => isRightTouchpadTouchedOnce;
    public float DeltaValueR => deltaValueR;



    void Start()
    {
        xrControllerAction = new XRIDefaultInputActions();
        xrControllerAction.Enable();
        xrControllerAction.XRIRightInteraction.Activate.performed +=  OnTriggerPressed;
        xrControllerAction.XRIRightInteraction.Deactivate.canceled +=  OnTriggerReleased;
        xrControllerAction.XRIRightInteraction.Select.performed +=  OnGripperPressed;
        xrControllerAction.XRIRightInteraction.TouchpadTouched.performed +=  OnTouchpadTouched;
        xrControllerAction.XRIRightInteraction.TouchPadRelease.performed +=  OnTouchpadReleased;
        xrControllerAction.XRILeftInteraction.TouchPadTouched.performed +=  OnTouchpadTouchedLeft; 
        xrControllerAction.XRILeftInteraction.TouchPadReleaseLeft.performed +=  OnTouchpadReleasedLeft;

    }

    private void OnTouchpadReleasedLeft(InputAction.CallbackContext context)
    {
        isLeftTouchpadTouchedOnce = false;
    }

    private void OnTouchpadTouchedLeft(InputAction.CallbackContext context)
    {
        isLeftTouchpadTouchedOnce = true;
        previousScrollYLeft = 0f;
    }

    void OnDestroy()
    {
        xrControllerAction.XRIRightInteraction.Activate.performed -=  OnTriggerPressed;
        xrControllerAction.XRIRightInteraction.Deactivate.canceled -=  OnTriggerReleased;
        xrControllerAction.XRIRightInteraction.Select.performed -=  OnGripperPressed;
        xrControllerAction.XRIRightInteraction.TouchpadTouched.performed -=  OnTouchpadTouched;
        xrControllerAction.XRIRightInteraction.TouchPadRelease.performed -=  OnTouchpadReleased;

        

        
    }
  

    private void OnTouchpadReleased(InputAction.CallbackContext context)
    {
       
       isRightTouchpadTouchedOnce = false;
       previousScrollYRight = 0f;
       deltaValueR = 0f;
       onTouchpadReleased.Invoke();
    }



    private void OnTouchpadTouched(InputAction.CallbackContext context)
    {
        
        isRightTouchpadTouchedOnce = true;
        onTouchpadTouched.Invoke();
    }

 
  

    private void OnGripperPressed(InputAction.CallbackContext context)
    {
        onGripperPressed.Invoke();
    }

   

    private void OnTriggerReleased(InputAction.CallbackContext context)
    {
        onTriggerPressed.Invoke();
    }

    private void OnTriggerPressed(InputAction.CallbackContext context)
    {
        onTriggerReleased.Invoke();
    }



  

    public float GetRightScrollDeltalValue()
    {

        
        
       

         Vector2 scrollValue = xrControllerAction.XRIRightInteraction.DirectionalManipulation.ReadValue<Vector2>();
        float currentScrollY = scrollValue.y;  // 今回のY成分
        float deltaY = currentScrollY - previousScrollYRight;  // Yの変化量を計算

        
        
        // 今回のY値を次回に使用するために保存
        previousScrollYRight = currentScrollY;
        
        return deltaY;
       
    }




    private float swipeThreshold = 0.8f;
    private float swipeCooldown = 0.3f;  
    private float lastSwipeTime = 0f; 


  
    public void GetIfLillyFlick()
    {

        
        if(!monitorInputConnection) return;
        
        Vector2 scrollValue = xrControllerAction.XRILeftInteraction.DirectionalManipulation.ReadValue<Vector2>();
        
        if (Time.time - lastSwipeTime < swipeCooldown)
            return;

        
        if (scrollValue.y > swipeThreshold)
        {
           onFlickLeftUp.Invoke();
          
            lastSwipeTime = Time.time;
        }
      
        else if (scrollValue.y < -swipeThreshold)
        {
            
            onFlickLeftDown.Invoke();
            lastSwipeTime = Time.time;


        }
    }


    private void Update() {
        
        if(isRightTouchpadTouchedOnce){
        
         deltaValueR = GetRightScrollDeltalValue();
         
        }

    }
    

}
