package com.pachonlabs.validateusingrae.controller.intent;

import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.params.ClientPNames;
import org.apache.http.client.params.CookiePolicy;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicHeader;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HTTP;
import org.apache.http.protocol.HttpContext;
import org.apache.http.util.EntityUtils;
import org.json.JSONException;
import org.json.JSONObject;

import android.util.Log;

import com.google.gson.Gson;

public class HTTPConnector {

	DefaultHttpClient httpClient;
	HttpContext localContext;
	private String ret;

	HttpResponse response = null;
	HttpPost httpPost = null;
	HttpGet httpGet = null;
	public final String JSON_TYPE = "application/json";
	
	
	/**
	 * @param webServiceUrl Nombre del servicio que será usado
	 */
	public HTTPConnector() {
		HttpParams myParams = new BasicHttpParams();

		HttpConnectionParams.setConnectionTimeout(myParams, 10000);
		HttpConnectionParams.setSoTimeout(myParams, 10000);
		httpClient = new DefaultHttpClient(myParams);
		localContext = new BasicHttpContext();
	}

	public String postREST(String urlString, String data, final String contentType) {
		ret = null;

		httpClient.getParams().setParameter(ClientPNames.COOKIE_POLICY, CookiePolicy.RFC_2109);

		httpPost = new HttpPost(urlString);
		response = null;

		StringEntity tmp = null;

		httpPost.setHeader(
				"Accept",
				"text/html,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5");

		if (contentType != null) {
			httpPost.setHeader("Content-Type", contentType);
		} else {
			httpPost.setHeader("Content-Type", "application/x-www-form-urlencoded");
		}

		try {
			tmp = new StringEntity(data, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			Log.e("Groshie", "HttpUtils : UnsupportedEncodingException : " + e);
		}

		httpPost.setEntity(tmp);

		Log.d("HTTPConnector", urlString + "?" + data);

		try {
			response = httpClient.execute(httpPost, localContext);

			if (response != null) {
				Log.d("HTTPConnector", "response");
				ret = EntityUtils.toString(response.getEntity());
			}
		} catch (Exception e) {
			Log.e("Groshie", "HttpUtils: " + e);
		}

		return ret;
	}

	
	public String getREST(String urlString) {
		httpGet = new HttpGet(urlString);
		Log.e("WebGetURL: ", urlString);

		try {
			response = httpClient.execute(httpGet);
		} catch (Exception e) {
			Log.e("Groshie:", e.getMessage());
		}

		try {
			ret = EntityUtils.toString(response.getEntity());
		} catch (IOException e) {
			Log.e("Groshie:", e.getMessage());
		}

		return ret;
	}

	public static JSONObject Object(Object o) {
		try {
			return new JSONObject(new Gson().toJson(o));
		} catch (JSONException e) {
			e.printStackTrace();
		}
		return null;
	}

	public InputStream getBinaryPOST(String urlString, String parameters, String contentType) {
		HttpResponse response;
		InputStream in = null;
        try{
            HttpPost post = new HttpPost(urlString);
            post.setHeader("Content-Type", "application/json");
            post.setHeader("Accept", "application/json");
            StringEntity se = new StringEntity(parameters);  
            se.setContentEncoding(new BasicHeader(HTTP.CONTENT_TYPE, contentType));
            post.setEntity(se);
            response = httpClient.execute(post);
            if(response!=null){
                in = response.getEntity().getContent(); 
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
		return in;
	}
	
	public static InputStream getBinaryGET(String urlString) throws IOException {
		InputStream in = null;
		int response = -1;
		URL url = new URL(urlString);
		URLConnection conn = url.openConnection();
		if (!(conn instanceof HttpURLConnection))
			throw new IOException("Not an HTTP connection");
		try {
			HttpURLConnection httpConn = (HttpURLConnection) conn;
			httpConn.setAllowUserInteraction(false);
			httpConn.setInstanceFollowRedirects(true);
			httpConn.setRequestMethod("GET");
			httpConn.connect();
			response = httpConn.getResponseCode();
			if (response == HttpURLConnection.HTTP_OK) {
				in = httpConn.getInputStream();
			}
		} catch (Exception ex) {
			throw new IOException(ex.getMessage());
		}
		return in;
	}
	
	
	public static InputStream getBinaryFromService(String urlServicio) {
		try {
			return getBinaryGET(urlServicio);
		} catch (Exception e) {
			System.out.println(e.getMessage());;
		}
		return null;
	}
	

	public void clearCookies() {
		httpClient.getCookieStore().clear();
	}

	
	public void abort() {
		try {
			if (httpClient != null) {
				httpPost.abort();
			}
		} catch (Exception e) {
			System.out.println(e);
		}
	}
	
	public String postBinary(String urlString, byte[] data, final String contentType) {
		ret = null;

		httpClient.getParams().setParameter(ClientPNames.COOKIE_POLICY, CookiePolicy.RFC_2109);

		httpPost = new HttpPost(urlString);
		response = null;

		ByteArrayEntity tmp = new ByteArrayEntity(data);;

		if (contentType != null) {
			httpPost.setHeader("Content-Type", contentType);
		} else {
			httpPost.setHeader("Content-Type", "application/x-www-form-urlencoded");
		}

		httpPost.setEntity(tmp);

		Log.d("HTTPConnector", urlString + "?" + data);

		try {
			response = httpClient.execute(httpPost, localContext);

			if (response != null) {
				Log.d("HTTPConnector", "response");
				ret = EntityUtils.toString(response.getEntity());
			}
		} catch (Exception e) {
			Log.e("Groshie", "HttpUtils: " + e);
		}

		return ret;
	}
}
