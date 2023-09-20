using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;

public class API : MonoBehaviour
{

    private string url;

    double var = 0;

    public GameObject carcost;
    public GameObject cartax;
    public GameObject cartime;
    public string carroute = "";

    public GameObject ctccost;
    public GameObject ctctax;
    public GameObject ctctime;
    public string ctcroute = "";

    public GameObject ctwcost;
    public GameObject ctwtax;
    public GameObject ctwtime;
    public string ctwroute = "";

    public GameObject wtccost;
    public GameObject wtctax;
    public GameObject wtctime;
    public string wtcroute = "";

    public GameObject wtwcost;
    public GameObject wtwtax;
    public GameObject wtwtime;
    public string wtwroute = "";

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void Call(int x1, int y1, int x2, int y2)
    {
        url = "https://2ec6-173-63-234-100.ngrok-free.app/main?start=[" + x1 + "," + y1 + "]&end=[" + x2 + "," + y2 + "]&time=[00,00]";
        StartCoroutine(GetData());
    }

    IEnumerator GetData()
    {
        using(UnityWebRequest request = UnityWebRequest.Get(url))
        {
            yield return request.SendWebRequest();

            if(request.result == UnityWebRequest.Result.ConnectionError)
            {
                Debug.Log("Connection Error");
            }
            else 
            {
                string result = request.downloadHandler.text;
                SimpleJSON.JSONNode json = SimpleJSON.JSON.Parse(result);
                
                SimpleJSON.JSONNode car = SimpleJSON.JSON.Parse((string)(json["Uber"]));
                Debug.Log(car);
                var = Math.Round((double)(car["cost"] * 100));
                var /= 100;
                carcost.GetComponent<TMP_Text>().text = "Price: $" + var;
                cartime.GetComponent<TMP_Text>().text = "Time: " + (int)(car["time"]);
                var = Math.Round((double)(car["env_tax"] * 100));
                var /= 100;
                cartax.GetComponent<TMP_Text>().text = "EcoTax: $" + var;
                carroute = car["route"];

                SimpleJSON.JSONNode ctc = SimpleJSON.JSON.Parse(json["Uber_Train_Uber"]);
                var = Math.Round((double)(ctc["cost"] * 100));
                var /= 100;
                ctccost.GetComponent<TMP_Text>().text = "Price: $" + var;
                ctctime.GetComponent<TMP_Text>().text = "Time: " + (int)(ctc["time"]);
                var = Math.Round((double)(ctc["env_tax"] * 100));
                var /= 100;
                ctctax.GetComponent<TMP_Text>().text = "EcoTax: $" + var;
                ctcroute = ctc["route"];

                SimpleJSON.JSONNode ctw = SimpleJSON.JSON.Parse(json["Uber_Train_Walk"]);
                var = Math.Round((double)(ctw["cost"] * 100));
                var /= 100;
                ctwcost.GetComponent<TMP_Text>().text = "Price: $" + var;
                ctwtime.GetComponent<TMP_Text>().text = "Time: " + (int)(ctw["time"]);
                var = Math.Round((double)(ctw["env_tax"] * 100));
                var /= 100;
                ctwtax.GetComponent<TMP_Text>().text = "EcoTax: $" + var;
                ctwroute = ctw["route"];

                SimpleJSON.JSONNode wtc = SimpleJSON.JSON.Parse(json["Walk_Train_Uber"]);
                var = Math.Round((double)(wtc["cost"] * 100));
                var /= 100;
                wtccost.GetComponent<TMP_Text>().text = "Price: $" + var;
                wtctime.GetComponent<TMP_Text>().text = "Time: " + (int)(wtc["time"]);
                var = Math.Round((double)(wtc["env_tax"] * 100));
                var /= 100;
                wtctax.GetComponent<TMP_Text>().text = "EcoTax: $" + var;
                wtcroute = wtc["route"];

                SimpleJSON.JSONNode wtw = SimpleJSON.JSON.Parse(json["Walk_Train_Walk"]);
                var = Math.Round((double)(wtw["cost"] * 100));
                var /= 100;
                wtwcost.GetComponent<TMP_Text>().text = "Price: $" + var;
                wtwtime.GetComponent<TMP_Text>().text = "Time: " + (int)(wtw["time"]);
                var = Math.Round((double)(wtw["env_tax"] * 100));
                var /= 100;
                wtwtax.GetComponent<TMP_Text>().text = "EcoTax: $" + var;
                wtwroute = wtw["route"];
            }
        }
    }
}
