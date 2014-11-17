package com.pachonlabs.validateusingrae;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;

import android.app.Activity;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.pachonlabs.validateusingrae.controller.RaeResponse;
import com.pachonlabs.validateusingrae.settings.LoadViewTask;
import com.pachonlabs.validateusingrae.settings.Loadingable;

public class MainActivity extends Activity implements Loadingable {

	public Button btnConsultar;
	public boolean val = false;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		setContentView(R.layout.main_layout);
		btnConsultar = (Button) findViewById(R.id.btnConsulta);

		btnConsultar.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {

				new LoadViewTask(MainActivity.this).execute();

			}
		});

	}

	@Override
	public void heavyTask() {
		BufferedReader reader = null;
		try {
			File dir = new File(Environment.getExternalStorageDirectory()
					+ File.separator + "CSV");
			dir.mkdirs();
			File fileCorrectos = new File(dir, "correctos.csv");
			fileCorrectos.createNewFile();

			File fileIncorrectos = new File(dir, "incorrectos.csv");

			fileIncorrectos.createNewFile();
			// write the bytes in file
			if (fileCorrectos.exists() && fileIncorrectos.exists()) {

				OutputStream foc = new FileOutputStream(fileCorrectos);
				OutputStream foi = new FileOutputStream(fileIncorrectos);
				reader = new BufferedReader(new InputStreamReader(getAssets()
						.open("output.csv")));

				String mLine = reader.readLine();
				while (mLine != null) {
					String parts[] = mLine.split("\\|");
					String linea = parts[3];
					String parts2[] = linea.split(" ");
					val = true;
					for (String i : parts2) {
						RaeResponse raeResponse = new RaeResponse(
								getApplication());
						String valor = raeResponse.ResponseRae(i);
						val = val
								&& valor.contains("definition single-definition");

					}
					if (val) {
						foc.write(mLine.getBytes());
						foc.write("\n".getBytes());
					} else {
						foi.write(mLine.getBytes());
						foi.write("\n".getBytes());
					}
					mLine = reader.readLine();
				}

				foc.close();
				foi.close();
			}
		} catch (Exception e) {
			Log.e("GG", e.toString());

		}

	}

	@Override
	public void afterTask() {

	}

}
