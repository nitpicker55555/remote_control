package com.example.socketclient;

import static android.opengl.Matrix.length;


import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Notification;
import android.app.NotificationManager;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.net.ConnectivityManager;
import android.net.Network;
import android.net.NetworkCapabilities;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.provider.Settings;
import android.text.TextUtils;
import android.util.Log;
import android.view.MotionEvent;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;

import android.view.View;
import android.view.WindowManager;
import android.view.animation.AccelerateInterpolator;
import android.view.animation.DecelerateInterpolator;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputMethodManager;
import android.widget.AutoCompleteTextView;
import android.widget.ListView;
import android.widget.PopupWindow;
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

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.SplittableRandom;
import java.util.TimerTask;
import java.util.concurrent.TimeUnit;

import io.netty.bootstrap.Bootstrap;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.ByteBufInputStream;
import io.netty.buffer.Unpooled;
import io.netty.channel.Channel;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelInboundHandlerAdapter;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioSocketChannel;
import io.netty.util.CharsetUtil;
import io.netty.util.Timeout;
import io.netty.util.Timer;

import android.view.animation.Interpolator;


@RequiresApi(api = Build.VERSION_CODES.R)
public class MainActivity extends AppCompatActivity implements View.OnTouchListener {
    private static final String PREFS_NAME = "MyApp_History";
    private static final String KEY_HISTORY = "input_history";

    private AutoCompleteTextView mip_text;
    private ArrayAdapter<String> adapter;
    private ArrayList<String> history;
    private static final int REQUEST_CODE_MANAGE_EXTERNAL_STORAGE_PERMISSION = 1;
    private int clickNum = 0;
    private static final int DOUBLE_CLICK_INTERVAL = 300; // 双击事件的时间间隔，单位为毫秒
    private static final long CLICK_INTERVAL_TIME = 300;
    private float lastX, lastY;
    private EditText mEditText,mEditText2,mEditText4,mEditText3;


    private TextView mStatusTextView, mMessageTextView;
    private Button mButton1, mButton2, mButton3, mButton4, mButton5,
            mButton6, mButton7, mButton8, mButton9, mButton10,mButton11,mButton12,mButton13,mButtonqr;
    private final String mServerIP = "130.61.253.72"; // 指定服务器 IP 地址
    private final int mServerPort = 1234; // 指定服务器端口号
    private Socket mSocket;
    private OutputStream mOutputStream;
    private AsyncTask<Void, String, Void> receiveTask;
    private BufferedReader mBufferedReader;
    private boolean mIsDarkMode = false;
    private final Handler mHandler = new Handler(Looper.getMainLooper());
    private NettyClient nettyClient;
    private ImageView imageView ,miv_bg;
    private ImageView imageView_picture ;
    private Bitmap bitmap;
    private static final int STORAGE_PERMISSION_CODE = 100;
    private  int stand_change=0;
    private  int stand_const=1;
    private  byte[] image_package;
    private  int image_package_int=0;
    private  int image_package_true=0;
    private int imageSize = 0;
    private int wordSize = 0;
    private String image_kind;
    private static final String TAG = "PERMISSION_TAG";
    private UdpClient udpClient;

    String[] options = { "get_clip","capture_image","capture_camera","win 3","win 1", "backspace","volumemute","volumeup","volumedown","shutdown_sever"};
    Handler handler = new Handler(Looper.getMainLooper());
    private static final String[] PERMISSIONS_STORAGE = {
            android.Manifest.permission.READ_EXTERNAL_STORAGE,
            android.Manifest.permission.MANAGE_EXTERNAL_STORAGE
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Spinner mySpinner = (Spinner) findViewById(R.id.mySpinner);
        mEditText = findViewById(R.id.editText);
        mip_text = findViewById(R.id.ip_text);
        mEditText2 = findViewById(R.id.editText2);
        mEditText3 = findViewById(R.id.editText3);
        mEditText4 = findViewById(R.id.editText4);
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
        mButton12= findViewById(R.id.button12);
        mButton13= findViewById(R.id.button13);
        mButtonqr= findViewById(R.id.button_qr);
        imageView  = findViewById(R.id.iv_stick);
        miv_bg  = findViewById(R.id.iv_bg);
        RotatingView rotatingView = findViewById(R.id.rotatingView);
        imageView_picture  = findViewById(R.id.picture);
        View view = findViewById(R.id.mainLayout); // 获取整个界面的布局
        imageView.setClickable(true);
        imageView.setOnTouchListener(this);
        miv_bg.setClickable(true);
        miv_bg.setOnTouchListener(this);
        imageView_picture.setClickable(true);


        if (isNetworkAvailable(this)) {
            showBubble("网络通畅");


        } else {
            showBubble("网络不通畅");
            // 尝试连接服务器
        }

        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, options);
        mySpinner.setAdapter(adapter);
        rotatingView.setRotationListener(this::sendUdpMessage);
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
                mEditText.requestFocus();
                InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
                imm.showSoftInput(mEditText, InputMethodManager.SHOW_IMPLICIT);
                return true;
            }
        });
        view.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String inputText = mEditText.getText().toString();
                if (inputText.trim().isEmpty()) {
                    // 输入内容为空或者只有空白字符
                    // 在这里处理内容为空的情况
                    System.out.println("EditText is empty");
                } else {
                    // 输入内容不为空
                    mButton8.performLongClick();


                    nettyClient.sendMessage("enter");
                }


            }
        });
        // 按钮1：显示桌面
        mip_text.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mip_text.showDropDown();
            }
        });

        ArrayAdapter<String> finalAdapter1 = adapter;
        mButtonqr.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View View) {
                String input = mip_text.getText().toString();
                if (!TextUtils.isEmpty(input) && !history.contains(input)) {
                    history.add(input);
                    saveHistory(history);
                    finalAdapter1.notifyDataSetChanged();
                }
                new Thread(() -> {
                    boolean isConnected = false;
                    while (!isConnected) {
                        try {
                            nettyClient = new NettyClient(mip_text.getText().toString(),1234);
                            nettyClient.run();
                            isConnected = true;  //连接成功，跳出循环
                            showBubble(mip_text.getText().toString()+" 端口1234");
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                            runOnUiThread(() -> mStatusTextView.setText("连接失败1"));
                            // 重试之前的等待时间，避免过度消耗资源
                            try {
                                Thread.sleep(2000);
                                showBubble("连接失败1 尝试重连");
                            } catch (InterruptedException interruptedException) {
                                interruptedException.printStackTrace();
                            }
                        } catch (Exception e) {
                            // 其他异常，显示错误消息
                            e.printStackTrace();
                            runOnUiThread(() -> mStatusTextView.setText("连接失败2"));
                            // 重试之前的等待时间，避免过度消耗资源
                            try {
                                Thread.sleep(2000);
                                showBubble("连接失败2 尝试重连");
                            } catch (InterruptedException interruptedException) {
                                interruptedException.printStackTrace();
                            }
                        }
                    }
                }).start();
            }
        });

        mButton1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                nettyClient.sendMessage("win d");

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
                //edd("ImageView Position"+ "Left: " + left + " Top: " + top + " Right: " + right + " Bottom: " + bottom+ " x: " + x+ " y: " + y);

            }
        });

        // 按钮2：tab
        mButton11.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                nettyClient.sendMessage("click");
            }
        });
        miv_bg.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                nettyClient.sendMessage("click");
            }
        });

        mButton11.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                nettyClient.sendMessage("rightclick");
                return true;
            }
        });
        mButton2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(stand_const==1){
                    nettyClient.sendMessage("ctrl shift tab");
                }
                else {
                    nettyClient.sendMessage("left");
                }
            }
        });
        mButton1.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                nettyClient.sendMessage("win tab");
                return true;
            }
        });
        mButton2.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                if(stand_const==1){
                    nettyClient.sendMessage("left");
                }
                else {
                    nettyClient.sendMessage("win left");
                }
                return true;
            }
        });
        mButton3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(stand_const==1){
                    nettyClient.sendMessage("ctrl tab");
                }
                else {
                    nettyClient.sendMessage("right");
                }
            }
        });
        mButton3.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                if(stand_const==1){
                    nettyClient.sendMessage("right");
                }
                else {
                    nettyClient.sendMessage("win right");
                }
                return true;
            }
        });
        mButton5.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(stand_const==1){
                    nettyClient.sendMessage("pagedown");
                }
                else {
                    nettyClient.sendMessage("down");
                }
            }
        });
        mButton5.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                nettyClient.sendMessage("win down");
                return true;
            }
        });
        mButton6.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                nettyClient.sendMessage("tab");
            }
        });
        mButton6.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                nettyClient.sendMessage("enter");
                return true;
            }
        });
        mButton4.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(stand_const==1){
                    nettyClient.sendMessage("pageup");
                }
                else {
                    nettyClient.sendMessage("up");
                }
            }
        });
        mButton4.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                nettyClient.sendMessage("win up");
                return true;
            }
        });
        mButton8.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = mEditText.getText().toString();
                nettyClient.sendMessage(message);
            }
        });
        mButton8.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                String message = mEditText.getText().toString()+"##";
                nettyClient.sendMessage(message);
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
                            nettyClient.sendMessage("playpause");
                        }else if(clickNum==2){
                            nettyClient.sendMessage("music_start");
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
                nettyClient.sendMessage("nexttrack");
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
                            nettyClient.sendMessage("esc");
                        }else if(clickNum==2){
                            AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                            builder.setTitle("确认");
                            builder.setMessage("确定要执行该任务吗？");
                            builder.setPositiveButton("确定", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialog, int which) {
                                    // 用户点击确定，执行任务
                                    nettyClient.sendMessage("shut_computer");
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
        imageView_picture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // 加载原图
                //File file = new File(Environment.getExternalStorageDirectory(), "image.png"); // 外部存储器中的图片路径
                File imagePath = new File(Environment.getExternalStorageDirectory(), "image.png"); // 创建Uri对象
//                openImage(imagePath);
            }
        });
        mButton10.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                nettyClient.sendMessage("alt f4");
                return true;
            }
        });
        mButton12.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = mEditText3.getText().toString();
                nettyClient.sendMessage(message);
            }
        });
        mButton12.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                //String message = mEditText3.getText().toString()+","+mEditText.getText().toString()+"##"+",enter";

                nettyClient.sendMessage("capture_camera");
                return true;
            }
        });
        int count = 0; // 计数器初始化为 0
        mButton13.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String message = mEditText4.getText().toString();
                nettyClient.sendMessage(message);
            }
        });
        mButton13.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                stand_change++; // 计数器加 1
                // 判断计数器的值是奇数还是偶数
                if (stand_change % 2 == 0) {
                    stand_const=1;
                    mButton13.setText(":-\uD83C\uDF1E                       ");
                    //mMessageTextView.setText("stand_mode is 1");
                } else {
                    stand_const=2;
                    mButton13.setText(":- \uD83C\uDF27                       ");
                    //mMessageTextView.setText("stand_mode is 2");
                }

                //nettyClient.sendMessage(message);
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
        history = loadHistory();

        adapter = new ArrayAdapter<>(this, android.R.layout.simple_dropdown_item_1line, history);
        mip_text.setAdapter(adapter);

        ArrayAdapter<String> finalAdapter = adapter;
        mip_text.setOnEditorActionListener((v, actionId, event) -> {
            if (actionId == EditorInfo.IME_ACTION_DONE) {
                String input = mip_text.getText().toString();
                if (!history.contains(input)) {
                    history.add(input);
                    saveHistory(history);
                    finalAdapter.notifyDataSetChanged();

                }
            }
            return false;
        });
    }
    private ArrayList<String> loadHistory() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        String savedHistory = prefs.getString(KEY_HISTORY, "");
        Log.d(TAG, savedHistory+"savedHistory:");
        return new ArrayList<>(Arrays.asList(savedHistory.split(",")));
    }

    private void saveHistory(ArrayList<String> historyList) {
        Log.d(TAG, historyList+"historyList:");

        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        SharedPreferences.Editor editor = prefs.edit();
        editor.putString(KEY_HISTORY, TextUtils.join(",", historyList));
        editor.apply();
    }
    public boolean isNetworkAvailable(Context context) {
        // 获取系统服务
        ConnectivityManager cm = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            // 获取当前活动的网络
            Network activeNetwork = cm.getActiveNetwork();

            if (activeNetwork != null) {
                // 检测当前网络是否可用
                NetworkCapabilities capabilities = cm.getNetworkCapabilities(activeNetwork);

                if (capabilities != null) {
                    if (capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR)
                            || capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)) {
                        // 网络连接可用
                        return true;
                    }
                }
            }
        } else {
            // 获取所有网络信息
            Network[] networks = cm.getAllNetworks();

            for (Network network : networks) {
                // 检测当前网络是否可用
                NetworkCapabilities capabilities = cm.getNetworkCapabilities(network);

                if (capabilities != null) {
                    if (capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR)
                            || capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)) {
                        // 网络连接可用
                        return true;
                    }
                }
            }
        }

        // 网络连接不可用
        return false;
    }
    public class NettyClient {

        private String host;
        private final int port;
        private ChannelFuture future;

        public NettyClient(String host, int port) {
            this.host = mip_text.getText().toString();
            this.port = 1234;
        }

        public void run() throws InterruptedException {
            // Maximum number of retry attempts
            int maxRetryAttempts = 7;
            int retryCount = 0;

            while (retryCount < maxRetryAttempts) {
                // Create an event loop group
                NioEventLoopGroup group = new NioEventLoopGroup();
                host = mip_text.getText().toString();
                try {
                    // Create a bootstrap for setting up the client
                    Bootstrap bootstrap = new Bootstrap();

                    // Configure the bootstrap
                    bootstrap.group(group)
                            .channel(NioSocketChannel.class)
                            .handler(new ChannelInitializer<SocketChannel>() {
                                @Override
                                public void initChannel(SocketChannel ch) {
                                    ch.pipeline().addLast(new NettyClientHandler());
                                }
                            });

                    // Connect to the server
                    future = bootstrap.connect(host, port).sync();
                    runOnUiThread(() -> mStatusTextView.setText("连接成功3"));

                    // Wait for the channel to close
                    future.channel().closeFuture().sync();
                    break;

                } catch (InterruptedException e) {

                    e.printStackTrace();
                    retryCount++;
                    showBubble(String.valueOf(retryCount)+"retry"+host);
                    if (retryCount >= maxRetryAttempts) {
                        throw e; // Rethrow the exception if maximum retry attempts reached
                    }

                } catch (Exception e) {
                    // 其他异常，显示错误消息
                    e.printStackTrace();
                    runOnUiThread(() -> mStatusTextView.setText("连接失败3"));
                    retryCount++;
                    showBubble(String.valueOf(retryCount)+"retry  "+host);
                    Thread.sleep(300);
                } finally {
                    // Shut down the event loop group
                    group.shutdownGracefully();
                }
            }
        }

        //照片的接收是分为很多package，一次就接收那么多，再循环接收也是-1!!!!!!所以为什么if png else 会失效，就因为数据包不是一次性来的！！！！！
        private class NettyClientHandler extends ChannelInboundHandlerAdapter {
            @RequiresApi(api = Build.VERSION_CODES.R)
            @Override
            public void channelRead(ChannelHandlerContext ctx, Object msg) throws InterruptedException, IOException {
                ByteBuf response = (ByteBuf) msg;


                if (image_package_int==0){
                    ByteBuf byteBuf = response.slice(0, 4).order(ByteOrder.LITTLE_ENDIAN);
                    byte[] bytes = new byte[4];
                    byteBuf.readBytes(bytes);
                    image_kind = new String(bytes, StandardCharsets.UTF_8);
                    System.out.println("Received kind: " + image_kind);
                    if (image_kind.equals("came") || (image_kind.equals("tmbb")) || (image_kind.equals("Bgdd"))){
                        ByteBuffer byteBuffer = response.slice(4, 8).order(ByteOrder.LITTLE_ENDIAN).nioBuffer();
                        imageSize = byteBuffer.getInt();
                        System.out.println("Received imageSize: " + imageSize);
                        response = response.slice(8, response.readableBytes() - 8);

                    } else if (image_kind.equals("wenz")|| (image_kind.equals("comp"))) {


                        ByteBuffer byteBuffer = response.slice(4, 8).order(ByteOrder.LITTLE_ENDIAN).nioBuffer();
                        wordSize = byteBuffer.getInt();
                        if (wordSize<1000){
                            System.out.println("Received wordSize: " + wordSize);
                            response = response.slice(8, response.readableBytes() - 8);
                            ByteBuf byteBuf_wenz = response.slice(0, wordSize).order(ByteOrder.LITTLE_ENDIAN);
                            String wenz =byteBuf_wenz.toString(CharsetUtil.UTF_8);
                            System.out.println("receive data   "+wenz);

                            runOnUiThread(() -> mEditText2.setText(wenz));
                            wordSize=0;
                        }


                    }


                }
                if (imageSize!=0){

                    try (//将非图片数据传入mEditText2
                         InputStream inputStream = new ByteBufInputStream(response)){

                        int rest_data;
                        rest_data=response.readableBytes();
                        System.out.println("rest_data:"+rest_data+"rest_imageSize:"+(imageSize-rest_data));
                        if (rest_data>10){
                            int step_length=Math.min(rest_data,imageSize-image_package_int);

                            ByteArrayOutputStream outputStream2 = new ByteArrayOutputStream( );

                            // Handle the response from the server
                            //runOnUiThread(() -> mEditText2.setText(data));
                            byte[] buffer = new byte[1024];
                            //byte[] buffer_end=new byte[imageSize];
                            int bytesRead = 0;
                            int bytesumme=0;
                            //boolean stand=false;
                            boolean hasReceivedEnough = false;
                            while ( !hasReceivedEnough) {
                                if (step_length-bytesumme!=0) {


                                    if (bytesRead==-1) {
                                        hasReceivedEnough=true;
                                    }


                                    try {

                                        bytesRead = inputStream.read(buffer, 0, Math.min(buffer.length, (step_length - bytesumme)));
                                    } catch (IOException e) {
                                        throw new RuntimeException(e);
                                    }
                                    outputStream2.write(buffer,0, bytesRead);
                                    bytesumme=bytesumme+bytesRead;
                                    System.out.println("step_length"+(step_length)+"bytesumme"+(bytesumme)+"---"+(step_length-bytesumme));

                                    System.out.println("buffer.length"+(buffer.length));
                                    System.out.println("bytesRead"+bytesRead);
                                }
                                else {
                                    hasReceivedEnough=true;
                                }

                            }
                            byte[] c= outputStream2.toByteArray( );

                            System.out.println("c ---length: "+c.length);
                            System.out.println("bytesumme  "+bytesumme);
                            merge(c);
                            image_package_int+=bytesumme;
                            image_package_true+=rest_data;
                            System.out.println("image_package.length:  "+image_package.length);
                            System.out.println("image_package_int:  "+image_package_int);
                            System.out.println("image_package_true:  "+image_package_true+"imageSize:"+imageSize);

                            if (image_package!=null){
                                if (image_package.length-imageSize>=0)
                                {
                                    createFolder(image_package);
                                    try {
                                        if (image_package_true-image_package_int!=0 && Objects.equals(image_kind, "tmbb")){
                                            bytesRead = inputStream.read(buffer, 0, image_package_true-image_package_int);
                                            String wenz = new String(buffer, 0, bytesRead);
                                            System.out.println("receive data   "+wenz);
                                            runOnUiThread(() -> mEditText2.setText(wenz));
                                        }


                                    } catch (IOException e) {
                                        throw new RuntimeException(e);
                                    }
                                    image_package=null;
                                    image_package_int=0;
                                    image_package_true=0;
                                    imageSize=0;
                                    System.out.println("receive finish");



                                }}



                        }  {
                            response.release();
                        }

                    }catch (Exception e) {
                        // 其他异常，显示错误消息
                        e.printStackTrace();
                        runOnUiThread(() -> mStatusTextView.setText("连接失败2"));
                    }
                }
                else{
                    String wenz =response.toString(CharsetUtil.UTF_8);
                    System.out.println("receive data   "+wenz);
                    if (!wenz.contains("get it")){
                        copyToClipboard(wenz);
                        if(wenz.contains("http")){
                            Log.d("acc","http存在 " +wenz);
                            openWebPage(wenz);
                        }
                    }
                    runOnUiThread(() -> mEditText2.setText(wenz));
                }}
        }



        public void merge(byte[] newData) {
            if (image_package!=null) {
                byte[] mergedData = new byte[image_package.length + newData.length];
                System.arraycopy(image_package, 0, mergedData, 0, image_package.length);
                System.arraycopy(newData, 0, mergedData, image_package.length, newData.length);
                image_package = mergedData;
            }
            else{
                image_package=newData;
            }
        }
        public void sendMessage(String message) {
            // Get the channel to the server
            message="___s"+message+"___e";
            Channel channel = future.channel();

            // Create a byte buffer with the message
            ByteBuf buf = Unpooled.copiedBuffer(message.getBytes());

            // Write the message to the channel
            channel.writeAndFlush(buf);
        }
        public void main(String[] args) throws Exception {
            NettyClient client = new NettyClient(host, port);
            // Run the client
            client.run();
        }
    }







    public void writeToFile(byte[] byteArray) throws IOException {
        File file = new File(Environment.getExternalStorageDirectory(), "image.png");
        FileOutputStream outputStream = new FileOutputStream(file);
        outputStream.write(byteArray);
        outputStream.close();
    }
    private void showBubble(String message) {
        runOnUiThread(() -> Toast.makeText(MainActivity.this, message, Toast.LENGTH_SHORT).show());
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
                //edd(Double.toString(xx)+","+Double.toString(yy)+"sb");
                sendUdpMessage(Double.toString(xx)+","+Double.toString(yy));
//                nettyClient.sendMessage(Double.toString(xx)+","+Double.toString(yy)+"sb");
                break;
            case MotionEvent.ACTION_UP:
                // 手指松开时，让控件返回初始位置
                sendUdpMessage("mouse_reset");
                imageView.animate().x(610).y(1716).setDuration(100).start();
                break;
        }
        return true;
    }


//    private void openImage(File imagePath) {
//        // 创建Uri对象
//
//
//        // 创建Intent对象
//
//        Uri contentUri = FileProvider.getUriForFile(this, BuildConfig.APPLICATION_ID + ".fileprovider", imagePath);
//
//        Intent intent = new Intent();
//        intent.setAction(Intent.ACTION_VIEW);
//        intent.setDataAndType(contentUri, "image/*");
//        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
//
//        if (intent.resolveActivity(getPackageManager()) != null) {
//            startActivity(intent);
//        } else {
//            Toast.makeText(this, "No app available to view image", Toast.LENGTH_SHORT).show();
//        }
//    }

    private void createFolder(byte[] byteArray){
        //get folder name

        try {
            File file = new File(Environment.getExternalStorageDirectory(), "image.png");
            FileOutputStream outputStream = new FileOutputStream(file);
            outputStream.write(byteArray);
            outputStream.close();
            bitmap = BitmapFactory.decodeFile(file.getAbsolutePath());
            //System.out.println("Received image: " + imageName + ", size: " + bytesRead.length);
            if (bitmap != null) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        imageView_picture.setImageBitmap(bitmap);
                        imageView_picture.bringToFront();
                        System.out.println("success to decode image");
                    }
                });
            } else {
                System.out.println("Failed to decode image");
            }
        } catch (IOException e) {
            // 如果保存过程中出现错误，则显示错误信息
            Toast.makeText(this, "保存失败：" + e.getMessage(), Toast.LENGTH_LONG).show();
        }
        //show if folder created or not


    }

    private ActivityResultLauncher<Intent> storageActivityResultLauncher = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            new ActivityResultCallback<ActivityResult>() {
                @Override
                public void onActivityResult(ActivityResult result) {
                    Log.d(TAG, "onActivityResult: ");
                    //here we will handle the result of our intent
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R){
                        //Android is 11(R) or above
                        if (Environment.isExternalStorageManager()){
                            //Manage External Storage Permission is granted
                            Log.d(TAG, "onActivityResult: Manage External Storage Permission is granted");
                            //createFolder();
                        }
                        else{
                            //Manage External Storage Permission is denied
                            Log.d(TAG, "onActivityResult: Manage External Storage Permission is denied");
                            Toast.makeText(MainActivity.this, "Manage External Storage Permission is denied", Toast.LENGTH_SHORT).show();
                        }
                    }
                    else {
                        //Android is below 11(R)
                    }
                }
            }
    );

    public boolean checkPermission(){
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R){
            //Android is 11(R) or above
            return Environment.isExternalStorageManager();
        }
        else{
            //Android is below 11(R)
            int write = ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE);
            int read = ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE);

            return write == PackageManager.PERMISSION_GRANTED && read == PackageManager.PERMISSION_GRANTED;
        }
    }

    /*Handle permission request results*/
    public void openWebPage(String url) {
        Intent intent = new Intent(Intent.ACTION_VIEW);
        intent.setData(Uri.parse(url));
        startActivity(intent);
    }
    public void copyToClipboard(String text) {
        ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
        ClipData clip = ClipData.newPlainText("label", "phone_clip_web"+text);
        if (text.contains("http")){
            clip = ClipData.newPlainText("label", "phone_clip_web: "+text);
        }
        else {
             clip = ClipData.newPlainText("label", text);
        }

        clipboard.setPrimaryClip(clip);
    }
    @SuppressLint("StaticFieldLeak")
    private void sendUdpMessage(String message) {
        // 考虑到我们之前讨论的，sendMessage 方法可能会阻塞,
        // 我们应该在后台线程上执行这个方法，以避免阻塞主线程。
//        new AsyncTask<String, Void, Void>() {
//            @Override
        if (udpClient==null){
            udpClient = new UdpClient(mip_text.getText().toString());
        }

        if (!message.contains(",")){
            if(stand_const==1){
                message+="quick";
            }
        }

        udpClient.sendMessage(message);
//        Log.d("Mainactivity==",message);
        Log.d("Mainactivity==",message);
//        return null;
    }
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == STORAGE_PERMISSION_CODE){
            if (grantResults.length > 0){
                //check each permission if granted or not
                boolean write = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                boolean read = grantResults[1] == PackageManager.PERMISSION_GRANTED;

                if (write && read){
                    //External Storage permissions granted
                    Log.d(TAG, "onRequestPermissionsResult: External Storage permissions granted");
                    //createFolder();
                }
                else{
                    //External Storage permission denied
                    Log.d(TAG, "onRequestPermissionsResult: External Storage permission denied");
                    Toast.makeText(this, "External Storage permission denied", Toast.LENGTH_SHORT).show();
                }
            }
        }
    }
    private void edd(final String message) {
        mEditText.setText(message);
        // Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
    }
    private void edd2(final String message) {
        runOnUiThread(() ->  mEditText2.setText(message));
        //Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
    }

    // 发送消息到服务器




    // 接收并处理来自服务器的消息


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