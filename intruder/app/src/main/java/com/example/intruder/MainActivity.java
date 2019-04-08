package com.example.intruder;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.TimePicker;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.Map;

public class MainActivity extends AppCompatActivity {

    //FirebaseDatabase database = FirebaseDatabase.getInstance();
    //DatabaseReference myRef = database.getReference("time");

    private Button mSendData;
    private Button act2;
    private Button start_time;
    private Button end_time;
    private TextView txt;
    TimePicker timePicker;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //mSendData = findViewById(R.id.add);
        act2 = findViewById(R.id.activity2);
        start_time = findViewById(R.id.button_start);
        end_time = findViewById(R.id.button_end);

        txt = findViewById(R.id.str);

        act2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivity2();
            }
        });

        start_time.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivityclockStart();


            }
        });

        end_time.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openActivityclockEnd();


            }
        });

//        mSendData.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                myRef.setValue("Hello, World!");
//
//            }
//        });
//
//        // Read from the database
//        myRef.addValueEventListener(new ValueEventListener() {
//            @Override
//            public void onDataChange(DataSnapshot dataSnapshot) {
//                // This method is called once with the initial value and again
//                // whenever data at this location is updated.
//                String value = dataSnapshot.getValue(String.class);
//
//                //Map<String, String> map = (Map)dataSnapshot.getValue();﻿
//
//
//
//                //   Log.d(TAG, "Value is: " + value);
//                txt.setText(value);
//            }
//
//            @Override
//            public void onCancelled(DatabaseError error) {
//                // Failed to read value
//                //   Log.w(TAG, "Failed to read value.", error.toException());
//            }
//        });





    }

    public void openActivity2(){
        Intent intent = new Intent(this, activity2.class);
        startActivity(intent);
    }

    public void openActivityclockStart(){
        Intent intent = new Intent(this, clockStart.class);
        startActivity(intent);
    }

    public void openActivityclockEnd(){
        Intent intent = new Intent(this, clockEnd.class);
        startActivity(intent);
    }

}
