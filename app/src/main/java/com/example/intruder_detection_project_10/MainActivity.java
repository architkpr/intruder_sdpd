package com.example.intruder_detection_project_10;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }


    public void launch_clock(View view) {
        Intent intent  = new Intent(this, clock1.class);
        this.startActivity(intent);
    }
}
