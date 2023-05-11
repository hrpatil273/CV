import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mega_project/models/chat_message.dart';


class ChatBubble extends StatefulWidget{
  ChatMessage chatMessage;
  ChatBubble({required this.chatMessage});
  @override
  _ChatBubbleState createState() => _ChatBubbleState();
}

class _ChatBubbleState extends State<ChatBubble> {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.only(left: 16, right: 16, top: 10, bottom: 10),
      child: Align(
        alignment: (Alignment.topRight),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(30),
            color: (Colors.grey.shade200),
          ),
          padding: EdgeInsets.all(16),
          child: Column(
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.only(bottom: 8.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: <Widget>[
                    Text(widget.chatMessage.date),
                    Text(widget.chatMessage.time),
                  ],
                ),
              ),
              Image.network(widget.chatMessage.image),
              Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: widget.chatMessage.name == "No One" ? Text("Hello Admin, Welcome to the online D-EYE Notifier! In this format you will able to see the future messages") :
                widget.chatMessage.name == "Unknown" ? Text("Hello Admin, This unknown person is waiting on your door") :
                Text("Hello Admin, "+widget.chatMessage.name+" have unlocked your door") ,
              ),
            ],
          ),
        ),
      ),
    );
  }
}