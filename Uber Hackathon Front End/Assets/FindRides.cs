using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class FindRides : MonoBehaviour
{

    public GameObject x1;
    public GameObject y1;
    public GameObject x2;
    public GameObject y2;
    public GameObject api;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void Find()
    {
        int ix1 = Int32.Parse(x1.GetComponent<TMP_Text>().text.Substring(0, x1.GetComponent<TMP_Text>().text.Length - 1));
        int iy1 = Int32.Parse(y1.GetComponent<TMP_Text>().text.Substring(0, y1.GetComponent<TMP_Text>().text.Length - 1));
        int ix2 = Int32.Parse(x2.GetComponent<TMP_Text>().text.Substring(0, x2.GetComponent<TMP_Text>().text.Length - 1));
        int iy2 = Int32.Parse(y2.GetComponent<TMP_Text>().text.Substring(0, y2.GetComponent<TMP_Text>().text.Length - 1));
        api.GetComponent<API>().Call(ix1, iy1, ix2, iy2);
    }
}
