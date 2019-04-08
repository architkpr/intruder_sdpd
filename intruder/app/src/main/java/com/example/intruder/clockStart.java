package com.example.intruder;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TimePicker;
import android.widget.Toast;
import android.widget.TextView;
import java.util.Calendar;


public class clockStart extends AppCompatActivity {


    private TextView txt;
    TimePicker timePicker;
    String time;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_clock_start);

        timePicker = findViewById(R.id.time_picker);
        txt = findViewById(R.id.text_time);
        Button button = findViewById(R.id.button_alarm);


        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Calendar calendar = Calendar.getInstance();

                calendar.set(
                        calendar.get(Calendar.YEAR),
                        calendar.get(Calendar.MONTH),
                        calendar.get(Calendar.DAY_OF_MONTH),
                        timePicker.getHour(),
                        timePicker.getMinute(),
                        0
                );
                time = "Start time has been set as " + String.valueOf(timePicker.getHour()) + ":" + String.valueOf(timePicker.getMinute());
                txt.setText(time);

                SharedPreferences sharedPref = getSharedPreferences("time_pref", Context.MODE_PRIVATE);
                SharedPreferences.Editor editor = sharedPref.edit();
                editor.putString("time", time);
                editor.apply();

                setAlarm(calendar.getTimeInMillis());

            }


        });





    }


    @Override
    protected void onResume() {
        super.onResume();

        SharedPreferences sharedPref = getSharedPreferences("time_pref", Context.MODE_PRIVATE);

        String time = sharedPref.getString("time", "");
        txt.setText(time);
    }


    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putString("time", time);

    }

    @Override
    protected void onRestoreInstanceState(Bundle savedInstanceState) {
        super.onRestoreInstanceState(savedInstanceState);
        time = savedInstanceState.getString("time");
        txt.setText(time);
    }

    private void setAlarm(long timeInMillis)
    {   String id ="start";
        AlarmManager alarmManager = (AlarmManager) getSystemService(Context.ALARM_SERVICE);

        Intent intent = new Intent(this, Alarm.class);
        intent.putExtra("EXTRA_SESSION_ID", id);

        PendingIntent pendingIntent = PendingIntent.getBroadcast(this, 0, intent, 0);

        alarmManager.set(AlarmManager.RTC_WAKEUP, timeInMillis, pendingIntent);


        Toast.makeText(this,"Start time set", Toast.LENGTH_SHORT).show();
    }
}
