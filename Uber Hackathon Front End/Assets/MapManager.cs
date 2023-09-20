using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MapManager : MonoBehaviour
{

    public GameObject intersection;
    public GameObject road;
    public Material carMat;
    public Material walkMat;
    public Material trainMat;
    private Material defaultMat;
    Quaternion rotation;
    Dictionary<string, GameObject> map;

    // Start is called before the first frame update
    void Start()
    {
        rotation.eulerAngles = new Vector3(0, 90, 0);
        map = new Dictionary<string, GameObject>();
        defaultMat = intersection.GetComponent<MeshRenderer>().material;
        Spawn();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void Spawn()
    {
        Vector3 location = new Vector3(-250, 0, -250);
        for(int i = 0; i < 100; i++)
        {
            for(int j = 0; j < 100; j++)
            {
                GameObject intobj = Instantiate(intersection, location, transform.rotation);
                map.Add("(" + i + "," + j + ")", intobj);
                if(i < 99)
                {
                    GameObject robj = Instantiate(road, new Vector3(location.x, location.y, location.z + 15), rotation);
                    map.Add("(" + i + "," + j + ")(" + (i + 1) + "," + j + ")", robj);
                    map.Add("(" + (i + 1) + "," + j + ")(" + i + "," + j + ")", robj);
                }
                location = new Vector3(location.x + 15, 0, location.z);
                if(j < 99)
                {
                    GameObject robj = Instantiate(road, location, transform.rotation);
                    map.Add("(" + i + "," + j + ")(" + i + "," + (j + 1) + ")", robj);
                    map.Add("(" + i + "," + (j + 1) + ")(" + i + "," + j + ")", robj);
                }
                location = new Vector3(location.x + 15, 0, location.z);
            }
            location = new Vector3(-250, 0, location.z + 30);
        }
    }

    void SetCarRoute(string route)
    {
        foreach(KeyValuePair<string, GameObject> entry in map)
        {
            entry.Value.GetComponent<MeshRenderer>().material = defaultMat;
        } 
        string[] path = route.Split(", ");
        for(int i = 0; i < path.Length; i++)
        {
            try
            {
                map[path[i]].GetComponent<MeshRenderer>().material = carMat;
            } catch(Exception e){}
            if(i < path.Length - 1)
            {
                try
                {
                    map[path[i] + path[i + 1]].GetComponent<MeshRenderer>().material = carMat;
                } catch(Exception e){}
            }
        }
    }

    void SetCTCRoute(string route)
    {
        foreach(KeyValuePair<string, GameObject> entry in map)
        {
            entry.Value.GetComponent<MeshRenderer>().material = defaultMat;
        } 
        string[] paths = route.Split("|");
        for(int i = 0; i < paths.Length; i++)
        {
            string[] path = paths[i].Split(", ");
            Material mat;
            if(i == 1)
            {
                mat = trainMat;
            }
            else
            {
                mat = carMat;
            }
            for(int j = 0; j < path.Length; j++)
            {
                try
                {
                    map[path[j]].GetComponent<MeshRenderer>().material = mat;
                } catch(Exception e){}
                if(j < path.Length - 1)
                {
                    try
                    {
                        map[path[j] + path[j + 1]].GetComponent<MeshRenderer>().material = mat;
                    } catch(Exception e){}
                }
            }
        }
    }

    void SetCTWRoute(string route)
    {
        foreach(KeyValuePair<string, GameObject> entry in map)
        {
            entry.Value.GetComponent<MeshRenderer>().material = defaultMat;
        } 
        string[] paths = route.Split("|");
        for(int i = 0; i < paths.Length; i++)
        {
            string[] path = paths[i].Split(", ");
            Material mat;
            if(i == 0)
            {
                mat = carMat;
            }
            else if(i == 1)
            {
                mat = trainMat;
            }
            else
            {
                mat = walkMat;
            }
            for(int j = 0; j < path.Length; j++)
            {
                try
                {
                    map[path[j]].GetComponent<MeshRenderer>().material = mat;
                } catch(Exception e){}
                if(j < path.Length - 1)
                {
                    try
                    {
                        map[path[j] + path[j + 1]].GetComponent<MeshRenderer>().material = mat;
                    } catch(Exception e){}
                }
            }
        }
    }

    void SetWTCRoute(string route)
    {
        foreach(KeyValuePair<string, GameObject> entry in map)
        {
            entry.Value.GetComponent<MeshRenderer>().material = defaultMat;
        } 
        string[] paths = route.Split("|");
        for(int i = 0; i < paths.Length; i++)
        {
            string[] path = paths[i].Split(", ");
            Material mat;
            if(i == 0)
            {
                mat = walkMat;
            }
            else if(i == 1)
            {
                mat = trainMat;
            }
            else
            {
                mat = carMat;
            }
            for(int j = 0; j < path.Length; j++)
            {
                try
                {
                    map[path[j]].GetComponent<MeshRenderer>().material = mat;
                } catch(Exception e){}
                if(j < path.Length - 1)
                {
                    try
                    {
                        map[path[j] + path[j + 1]].GetComponent<MeshRenderer>().material = mat;
                    } catch(Exception e){}
                }
            }
        }
    }

    void SetWTWRoute(string route)
    {
        foreach(KeyValuePair<string, GameObject> entry in map)
        {
            entry.Value.GetComponent<MeshRenderer>().material = defaultMat;
        } 
        string[] paths = route.Split("|");
        for(int i = 0; i < paths.Length; i++)
        {
            string[] path = paths[i].Split(", ");
            Material mat;
            if(i == 1)
            {
                mat = trainMat;
            }
            else
            {
                mat = walkMat;
            }
            for(int j = 0; j < path.Length; j++)
            {
                try
                {
                    map[path[j]].GetComponent<MeshRenderer>().material = mat;
                } catch(Exception e){}
                if(j < path.Length - 1)
                {
                    try
                    {
                        map[path[j] + path[j + 1]].GetComponent<MeshRenderer>().material = mat;
                    } catch(Exception e){}
                }
            }
        }
    }
    
}
