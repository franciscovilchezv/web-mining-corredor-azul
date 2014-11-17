package com.pachonlabs.validateusingrae.controller;

import android.content.Context;

import com.pachonlabs.validateusingrae.controller.intent.HTTPConnector;
import com.pachonlabs.validateusingrae.framework.controller.Controller;

public class RaeResponse extends Controller{

	public RaeResponse(Context context) {
		super(context);
	}
	
	public String ResponseRae(String termino){
		String resultado = "";
		HTTPConnector poster = new HTTPConnector();
		try{
			//String path = "http://buscon.rae.es/drae/srv/search?val=sencillo";
			String path = "http://www.spanishcentral.com/translate/" + termino;
			resultado = poster.getREST(path);
			
		}catch(Exception e){
			
		}
				
		return resultado;
	}
	

}
