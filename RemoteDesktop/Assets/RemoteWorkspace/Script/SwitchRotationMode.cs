using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit.UI;

public class SwitchRotationMode : MonoBehaviour
{


    private LazyFollow lazyFollow;
    // Start is called before the first frame update
    void Start()
    {
        lazyFollow = GetComponent<LazyFollow>();
    }
    


    public void SetNone() 
    {
        lazyFollow.rotationFollowMode = LazyFollow.RotationFollowMode.None; 
    }

    public void SetRotation() 
    {
        lazyFollow.rotationFollowMode = LazyFollow.RotationFollowMode.LookAtWithWorldUp; 
    }



}
