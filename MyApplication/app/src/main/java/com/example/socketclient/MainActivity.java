package com.example.socketclient;

import android.app.Notification;
import android.app.NotificationManager;
import android.content.Context;
import android.content.DialogInterface;
import android.content.res.Resources;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.MotionEvent;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.view.View;
import android.view.animation.AccelerateInterpolator;
import android.view.animation.DecelerateInterpolator;
import android.widget.TextView;
import android.os.Vibrator;
import android.util.AttributeSet;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.Socket;


import android.view.animation.Interpolator;


public class MainActivity extends AppCompatActivity implements View.OnTouchListener {
    private int clickNum = 0;
    private static final int DOUBLE_CLICK_INTERVAL = 300; // 双击事件的时间间隔，单位为毫秒
    private static final long CLICK_INTERVAL_TIME = 300;
    private float lastX, lastY;
    private EditText mEditText,mEditText2;


    private TextView mStatusTextView, mMessageTextView;
    private Button mButton1, mButton2, mButton3, mButton4, mButton5,
            mButton6, mButton7, mButton8, mButton9, mButton10,mButton11;
    private final String mServerIP = "130.61.253.72"; // 指定服务器 IP 地址
    private final int mServerPort = 1234; // 指定服务器端口号
    private Socket mSocket;
    private OutputStream mOutputStream;
    private AsyncTask<Void, String, Void> receiveTask;
    private BufferedReader mBufferedReader;
    private boolean mIsDarkMode = false;
    private final Handler mHandler = new Handler(Looper.getMainLooper());

    private ImageView imageView ;
    String[] options = {"shutdown_sever", "backspace", "win 3","win 1","volumemute"};
    Handler handler = new Handler(Looper.getMainLooper());


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Spinner mySpinner = (Spinner) findViewById(R.id.mySpinner);
        mEditText = findViewById(R.id.editText);
        mEditText2 = findViewById(R.id.editText2);
        mStatusTextView = findViewById(R.id.statusTextView);
        mMessageTextView = findViewById(R.id.messageTextView);
        mButton1 = findViewById(R.id.button1);
        mButton2 = findViewById(R.id.button2);
        mButton3 = findViewById(R.id.button3);
        mButton4 = findViewById(R.id.button4);
        mButton5 = findViewById(R.id.button5);
        mButton6 = findViewById(R.id.button6);
        mButton7 = findViewById(R.id.button7);
        mButton8 = findViewById(R.id.button8);
        mButton9 = findViewById(R.id.button9);
        mButton10 = findViewById(R.id.button10);
        mButton11= findViewById(R.id.button11);
        imageView  = findViewById(R.id.iv_stick);
        View view = findViewById(R.id.mainLayout); // 获取整个界面的布局
        imageView.setClickable(true);
        imageView.setOnTouchListener(this);



        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, options);
        mySpinner.setAdapter(adapter);

        mySpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                String selectedOption = (String) adapterView.getItemAtPosition(i);
                mEditText.setText(selectedOption);
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
                // Do nothing
            }

        });



// 单击事件处理函数


        view.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                mEditText.setText("");
                return true;
            }
        });
        // 按钮1：显示桌面
        mButton1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendMsg("win d");

                int[] location = new int[2];
                imageView.getLocationOnScreen(location);
                int x = location[0];
                int y = location[1];
                int width = imageView.getWidth();
                int height = imageView.getHeight();

                // 计算 ImageView 控件的位置和尺寸信息
                int left = x;
                int top = y;
                int right = x + width;
                int bottom = y + height;

                // 输出 ImageView 控件距离屏幕四边的距离
               // edd("ImageView Position"+ "Left: " + left + " Top: " + top + " Right: " + right + " Bottom: " + bottom+ " x: " + x+ " y: " + y);

            }
        });

        // 按钮2：tab
        mButton11.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendMsg("click");
            }
        });

        mButton11.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                sendMsg("doubleclick");
                return true;
            }
        });
        mButton2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendMsg("ctrl shift tab");
            }
        });
        mButton1.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                sendMsg("win tab" +
                        "");
                return true;
            }
        });
        mButton2.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                sendMsg("left");
                return true;
            }
        });
        mButton3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendMsg("ctrl tab");
            }
        });
        mButton3.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                sendMsg("right");
                return true;
            }
        });
        mButton5.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendMsg("pagedown");
            }
        });
        mButton5.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                sendMsg("win down");
                return true;
            }
        });
        mButton6.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendMsg("tab");
            }
        });
        mButton6.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                sendMsg("enter");
                return true;
            }
        });
        mButton4.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendMsg("pageup");
            }
        });
        mButton4.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                sendMsg("win up");
                return true;
            }
        });
        mButton8.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = mEditText.getText().toString();
                sendMsg(message);
            }
        });
        mButton8.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                String message = mEditText.getText().toString()+"##";
                sendMsg(message);
                return true;
            }
        });

        mButton9.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                clickNum++;
                handler.postDelayed(new Runnable() {
                    @Override
                    public void run() {
                        if (clickNum == 1) {
                            sendMsg("playpause");
                        }else if(clickNum==2){
                            sendMsg("music_start");
                        }
                        //防止handler引起的内存泄漏
                        handler.removeCallbacksAndMessages(null);
                        clickNum = 0;
                    }
                },300);
            }
        });



        mButton9.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                sendMsg("nexttrack");
                return true;
            }
        });
        mButton10.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                clickNum++;
                handler.postDelayed(new Runnable() {
                    @Override
                    public void run() {
                        if (clickNum == 1) {
                            sendMsg("esc");
                        }else if(clickNum==2){
                            AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                            builder.setTitle("确认");
                            builder.setMessage("确定要执行该任务吗？");
                            builder.setPositiveButton("确定", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialog, int which) {
                                    // 用户点击确定，执行任务
                                    sendMsg("win d,alt f4,enter");
                                }
                            });
                            builder.setNegativeButton("取消", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialog, int which) {
                                    // 用户点击取消，取消执行任务
                                    Toast.makeText(MainActivity.this, "已取消关机", Toast.LENGTH_SHORT).show();

                                }
                            });
                            builder.show();
                        }
                        //防止handler引起的内存泄漏
                        handler.removeCallbacksAndMessages(null);
                        clickNum = 0;
                    }
                },300);
            }
        });
        mButton10.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                    sendMsg("alt f4");
                return true;
            }
        });
        // 按钮3：切换模式
        mButton7.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mIsDarkMode = !mIsDarkMode;
                updateUI();
            }
        });

        // 连接服务器
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    mSocket = new Socket(mServerIP, mServerPort);
                    mOutputStream = mSocket.getOutputStream();
                    mBufferedReader = new BufferedReader(new InputStreamReader(mSocket.getInputStream()));
                    mHandler.post(new Runnable() {
                        @Override
                        public void run() {
                            mStatusTextView.setText(String.format("连接成功，端口：%d", mServerPort));
                        }
                    });
                    while (true) {
                        final String message = mBufferedReader.readLine();
                        if (message != null) {
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    // 在这里更新UI组件，将服务器回传信息显示在文本框中
                                    mEditText2.setText(message + "\n");
                                    Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
                                }
                            });
                        }
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();


    }
    public boolean onTouch(View v, MotionEvent event) {
        float x = event.getRawX();
        float y = event.getRawY();
        float distance_x,distance_y;





        switch (event.getAction()) {
            case MotionEvent.ACTION_DOWN:
                // 手指按下时，记录当前位置
                lastX = x;
                lastY = y;

                break;
            case MotionEvent.ACTION_MOVE:
                // 手指移动时，计算位移并更新控件位置
                imageView.setX(x-140);  //380 2075 514 2117
                imageView.setY(y-340);
                distance_x=x-lastX;
                distance_y=y-lastY;
                String  str = String.format("%.2f",distance_x);
                double xx = Double.parseDouble(str);
                String  strr = String.format("%.2f",distance_y);
                double yy = Double.parseDouble(strr);
                edd(Double.toString(xx)+","+Double.toString(yy)+"sb");
                sendMsg(Double.toString(xx)+","+Double.toString(yy)+"sb");
                break;
            case MotionEvent.ACTION_UP:
                // 手指松开时，让控件返回初始位置
                imageView.animate().x(390).y(1766).setDuration(800).start();
                break;
        }
        return true;
    }

    private void edd(final String message) {
        mEditText.setText(message);
       // Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
    }
    private void edd2(final String message) {
        mEditText2.setText(message);
        //Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
    }

    // 发送消息到服务器
    private void sendMsg(final String message) {
        if (mSocket == null || !mSocket.isConnected()) {
            Toast.makeText(MainActivity.this, "未连接服务器", Toast.LENGTH_SHORT).show();
            return;
        }
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    OutputStream outputStream = mSocket.getOutputStream();
                    outputStream.write(message.getBytes());
                    outputStream.flush();
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            // 在这里更新UI组件
                            mEditText.setText(message);
                        }
                    });
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }


    // 接收并处理来自服务器的消息
    private void handleMessageFromServer(final String message) {
        mHandler.post(new Runnable() {
            @Override
            public void run() {

                mEditText2.setText(message);
                mMessageTextView.setText(message);
                Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
                // 发送通知
                // 获取Vibrator实例
                Vibrator vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);

// 震动指定毫秒数
                vibrator.vibrate(1000);

// 停止震动
                vibrator.cancel();
                Notification.Builder builder = new Notification.Builder(MainActivity.this);
                Resources res = MainActivity.this.getResources();
                String appName = res.getString(R.string.app_name);
                builder.setContentTitle(appName)
                        .setContentText(message)
                        .setSmallIcon(R.mipmap.ic_launcher);
                Notification notification = builder.build();
                NotificationManager notificationManager =
                        (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
                notificationManager.notify(0, notification);
            }
        });
    }

    // 更新界面样式
    private void updateUI() {
        if (mIsDarkMode) {
            mStatusTextView.setTextColor(Color.WHITE);
            mMessageTextView.setTextColor(Color.WHITE);
            mEditText.setTextColor(Color.WHITE);
            mEditText2.setTextColor(Color.WHITE);
            mButton1.setTextColor(Color.WHITE);
            mButton1.setBackgroundResource(R.drawable.button_dark);

            mButton2.setTextColor(Color.WHITE);
            mButton2.setBackgroundResource(R.drawable.button_dark);

            mButton3.setTextColor(Color.WHITE);
            mButton3.setBackgroundResource(R.drawable.button_dark);

            mButton4.setTextColor(Color.WHITE);
            mButton4.setBackgroundResource(R.drawable.button_dark);

            mButton5.setTextColor(Color.WHITE);
            mButton5.setBackgroundResource(R.drawable.button_dark);

            mButton6.setTextColor(Color.WHITE);
            mButton6.setBackgroundResource(R.drawable.button_dark);

            mButton8.setTextColor(Color.WHITE);
            mButton8.setBackgroundResource(R.drawable.button_dark);

            mButton9.setTextColor(Color.WHITE);
            mButton9.setBackgroundResource(R.drawable.button_dark);

            mButton10.setTextColor(Color.WHITE);
            mButton10.setBackgroundResource(R.drawable.button_dark);


            mButton7.setText("light");
            mButton7.setTextColor(Color.WHITE);
            mButton7.setBackgroundResource(R.drawable.button_dark);
            findViewById(R.id.mainLayout).setBackgroundColor(Color.DKGRAY);
        } else {
            mStatusTextView.setTextColor(Color.BLACK);
            mMessageTextView.setTextColor(Color.BLACK);
            mEditText.setTextColor(Color.BLACK);
            mEditText2.setTextColor(Color.BLACK);
            mButton1.setTextColor(Color.BLACK);
            mButton1.setBackgroundResource(R.drawable.button_light);
            mButton2.setTextColor(Color.BLACK);
            mButton2.setBackgroundResource(R.drawable.button_light);

            mButton3.setTextColor(Color.BLACK);
            mButton3.setBackgroundResource(R.drawable.button_light);

            mButton4.setTextColor(Color.BLACK);
            mButton4.setBackgroundResource(R.drawable.button_light);

            mButton5.setTextColor(Color.BLACK);
            mButton5.setBackgroundResource(R.drawable.button_light);

            mButton6.setTextColor(Color.BLACK);
            mButton6.setBackgroundResource(R.drawable.button_light);

            mButton8.setTextColor(Color.BLACK);
            mButton8.setBackgroundResource(R.drawable.button_light);

            mButton9.setTextColor(Color.BLACK);
            mButton9.setBackgroundResource(R.drawable.button_light);

            mButton10.setTextColor(Color.BLACK);
            mButton10.setBackgroundResource(R.drawable.button_light);

            mButton7.setText("dark");
            mButton7.setTextColor(Color.BLACK);
            mButton7.setBackgroundResource(R.drawable.button_light);
            findViewById(R.id.mainLayout).setBackgroundColor(Color.WHITE);
        }
    }}
