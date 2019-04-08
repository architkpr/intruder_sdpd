package com.example.intruder;


import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.media.MediaPlayer;
import android.provider.MediaStore;
import android.provider.Settings;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class Alarm_stop extends BroadcastReceiver
{

    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference myRef = database.getReference("Start");
    @Override
    public void onReceive(Context context, Intent intent)               // To be executed whenever alarm is fired
    {

        // String id= intent.getStringExtra("end");
        //String id= intent.getStringExtra("EXTRA_SESSION_ID");

        // Task to be done when alarm is fired
        //MediaPlayer mediaPlayer = MediaPlayer.create(context, Settings.System.DEFAULT_ALARM_ALERT_URI);
        //mediaPlayer.start()
        myRef.setValue("0");


    }
}