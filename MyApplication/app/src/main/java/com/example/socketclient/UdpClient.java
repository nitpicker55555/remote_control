package com.example.socketclient;
import android.annotation.SuppressLint;
import android.os.AsyncTask;
import android.util.Log;

import io.netty.bootstrap.Bootstrap;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.ByteBufAllocator;
import io.netty.channel.Channel;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.DatagramPacket;
import io.netty.channel.socket.nio.NioDatagramChannel;

import java.net.InetSocketAddress;

public class UdpClient {

    private final int port;
    private final String host;
    private Channel channel; // 保存Channel引用以便后续发送消息

    public UdpClient(String  host) {
        this.host = host;
        this.port = 8888;
        Log.d("UdpClient",host);
    }

    public void start() throws InterruptedException {
        Log.i("UdpClient", "Starting UdpClient...");

        EventLoopGroup group = new NioEventLoopGroup();
        try {
            Bootstrap b = new Bootstrap();
            b.group(group)
                    .channel(NioDatagramChannel.class)
                    .handler(new ChannelInitializer<Channel>() {
                        @Override
                        protected void initChannel(Channel ch) throws Exception {
                            ch.pipeline().addLast(new NettyUdpClientHandler());
                            Log.i("UdpClient", "Channel initialized with NettyUdpClientHandler");
                        }
                    });

            channel = b.bind(0).sync().channel(); // 绑定到任意本地端口

            if (channel != null) {
                Log.i("UdpClient", "Channel successfully bound to port: " + channel.localAddress());
                // 等待通道关闭
                channel.closeFuture().await();
            } else {
                Log.e("UdpClient", "Channel is null after binding");
            }

        } catch (Exception e) {
            Log.e("UdpClient", "Error in UdpClient start method", e);
        } finally {
            group.shutdownGracefully();
            Log.i("UdpClient", "EventLoopGroup shutdown gracefully");
        }
    }


    @SuppressLint("StaticFieldLeak")
    public void sendMessage(String message){
        Log.d("UdpClient",message);

        if (channel == null || !channel.isActive()) {
            new AsyncTask<Void, Void, Void>() {
                @Override
                protected Void doInBackground(Void... voids) {
                    try {
                        start();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                        Log.e("UdpClient",e.toString());
                    }
                    return null;
                }
            }.execute();


        }
        Log.e("UdpClient", "UdpClient");
        if (channel == null) {
            Log.e("UdpClient", "Channel is null");
        } else if (!channel.isActive()) {
            Log.e("UdpClient", "Channel is not active");
        }
        if (channel != null && channel.isActive()) {
            ByteBufAllocator byteBufAllocator = ByteBufAllocator.DEFAULT;
            DatagramPacket datagramPacket = new DatagramPacket(byteBufAllocator.buffer().writeBytes(message.getBytes()),
                    new InetSocketAddress(host, port));
            channel.writeAndFlush(datagramPacket);
            Log.e("UdpClient", "UdpClient send successfully");
        }
    }

    private static class NettyUdpClientHandler extends SimpleChannelInboundHandler<DatagramPacket> {
        @Override
        protected void channelRead0(ChannelHandlerContext ctx, DatagramPacket packet) throws Exception {
            ByteBuf content = packet.content();
            // 处理接收到的数据...
        }
    }

//    public static void main(String[] args) throws InterruptedException {
//        UdpClient client = new UdpClient();
//        client.start();
//
//        // 示例：使用sendMessage函数发送消息
//        client.sendMessage("Hello, Server!");
//    }
}
