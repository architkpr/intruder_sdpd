package com.example.intruder;

import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;


public class MainActivity extends AppCompatActivity {




    private Button act2;
    private Button start_time;
    private Button end_time;
    private TextView txt;
    private TextView active;

    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference myRef = database.getReference("Start/new");





    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        act2 = findViewById(R.id.activity2);
        start_time = findViewById(R.id.button_start);
        end_time = findViewById(R.id.button_end);

        txt = findViewById(R.id.textView);
        active = findViewById(R.id.active);

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
//
//        mSendData.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                myRef.setValue("Hello, World!");
//
//            }
//        });

        // Read from the database
        myRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {

                String start = dataSnapshot.getValue(String.class);
                if (start.equals("1")) {
                    active.setText("The detection system is presently active!");
                }
                else {
                    active.setText("The detection system is presently NOT active!");
                }

            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });





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
