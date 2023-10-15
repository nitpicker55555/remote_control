package com.example.socketclient;
import com.example.socketclient.UdpClient;
import android.content.Context;
import android.util.AttributeSet;
import android.util.Log;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.view.View;
import android.os.Vibrator;
public class RotatingView extends View {
    private float lastAngle = 0;
    private Vibrator vibrator;
    private float totalRotatedAngle = 0;
    private GestureDetector gestureDetector;
    private UdpClient udpclient;


    public RotatingView(Context context) {
        super(context);
        init();
//        udpclient = new UdpClient();
    }

    public RotatingView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
//        udpclient = new UdpClient();
    }

    public RotatingView(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();

    }

    public RotatingView(Context context, AttributeSet attrs, int defStyleAttr, int defStyleRes) {
        super(context, attrs, defStyleAttr, defStyleRes);
        init();

    }
    private void init() {
//        udpclient = new UdpClient();

        gestureDetector = new GestureDetector(getContext(), new GestureDetector.SimpleOnGestureListener() {
            @Override
            public boolean onDown(MotionEvent e) {
                Log.d("RotatingView", "onDown");
                return true; // 这是必须的，以确保我们可以接收到onScroll事件
            }

            @Override
            public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX, float distanceY) {
                float centerX = getWidth() / 2;
                float centerY = getHeight() / 2;

                float startAngle = (float) Math.toDegrees(Math.atan2(e1.getY() - centerY, e1.getX() - centerX));
                float endAngle = (float) Math.toDegrees(Math.atan2(e2.getY() - centerY, e2.getX() - centerX));

                float angle = endAngle - startAngle;
                if (angle < -180.f) angle += 360.0f;
                if (angle > 180.f) angle -= 360.0f;

                totalRotatedAngle += angle;

                if(Math.abs(totalRotatedAngle) >= 20){
                    vibrate();
                    if(totalRotatedAngle > 0) {
                        Log.d("RotatingView", "shun");
                        rotationListener.onRotation("down");
//
//                        udpclient.sendMessage("down");
                    } else {

                        Log.d("RotatingView", "ni");
                        rotationListener.onRotation("up");
//                        udpclient.sendMessage("up");
                    }
                    totalRotatedAngle %= 20;
                }

                setRotation(getRotation() + angle);
                lastAngle = angle;
                return true;
            }
        });
        vibrator = (Vibrator) getContext().getSystemService(Context.VIBRATOR_SERVICE);
    }
    public interface RotationListener {
        void onRotation(String direction);
    }
    private RotationListener rotationListener;

    public void setRotationListener(RotationListener listener) {
        this.rotationListener = listener;
    }
    private void vibrate() {
        if (vibrator.hasVibrator()) {
            vibrator.vibrate(20); // 震动100毫秒
        }
    }
    @Override
    public boolean onTouchEvent(MotionEvent event) {
        Log.d("RotatingView", "Touch event detected: " + event.getActionMasked());
        return gestureDetector.onTouchEvent(event) || super.onTouchEvent(event);
    }
}
