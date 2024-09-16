using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI; 

public class HandleClose : MonoBehaviour
{
    Image crossImage; 

    void Start()
    {
        this.crossImage = GetComponent<Image>();
    }
    public void ColorEnabled(bool enabled)
    {
        this.crossImage.color = enabled ? Color.white : Color.black;
    }


    public void OnClick() 
    {
        Debug.Log("Close");
    }
}
