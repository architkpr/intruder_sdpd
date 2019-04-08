package com.example.intruder;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class Alarm extends BroadcastReceiver
{

    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference myRef = database.getReference("Start/new");
    @Override
    public void onReceive(Context context, Intent intent)               // To be executed whenever alarm is fired
    {
        String id= intent.getStringExtra("EXTRA_SESSION_ID");

        if(id.equals("end"))
        {myRef.setValue("0");}
        else
        {myRef.setValue("1");}

    }
}

