package com.pachonlabs.validateusingrae.settings;

import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;
import android.view.Window;

public class LoadViewTask extends AsyncTask<Void, Integer, Void> {
	// Before running code in the separate thread
	Loadingable component;

	ProgressDialog pd;
	String message;
	Context _context;

	public LoadViewTask(Loadingable component) {
		this.component = component;
		this.message = "Cargando...";
		this._context = null;
	}
	
	public LoadViewTask(Loadingable component, Context _context) {
		this.component = component;
		this.message = "Cargando...";
		this._context = _context;
	}
	
	public LoadViewTask(Loadingable component, String message) {
		this.component = component;
		this.message = message;
		this._context = null;
	}

	@Override
	protected synchronized void onPreExecute() {
		if(this._context!=null){
			pd = new ProgressDialog(_context);
		}else{
			pd = new ProgressDialog((Context)component);
		}
		pd.setCancelable(false);
		pd.requestWindowFeature(Window.FEATURE_NO_TITLE);
		pd.setMessage(message);
		pd.show();

	}

	// The code to be executed in a background thread.
	@Override
	protected Void doInBackground(Void... params) {
		// Get the current thread's token
		synchronized (this) {
			component.heavyTask();
		}

		return null;

	}

	@Override
	protected void onPostExecute(Void result) {

		component.afterTask();

		if (pd.isShowing())
			pd.dismiss();

	}

}