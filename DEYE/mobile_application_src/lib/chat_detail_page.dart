import 'dart:async';

import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'components/chat_bubble.dart';
import 'components/chat_detail_page_appbar.dart';
import 'models/chat_message.dart';

enum MessageType{
  Sender,
  Receiver,
}


class ChatDetailPage extends StatefulWidget{
  @override
  _ChatDetailPageState createState() => _ChatDetailPageState();
}

final ChatMessagesReference = FirebaseDatabase.instance.reference();


class _ChatDetailPageState extends State<ChatDetailPage> {


  late List<ChatMessage> items;

  List<ChatMessage> item = [
  ChatMessage("XX  --,--",
  "https://www.google.com/url?sa=i&url=https%3A%2F%2Fdribbble.com%2Ftags%2F404-page&psig=AOvVaw3EKHfDzea0eFuSrfW4pKWh&ust=1592397105304000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCIi5hdGrhuoCFQAAAAAdAAAAABAu",
  "No One",
  "--:--")
  ];
  late StreamSubscription<Event> _onChatMessageAddedSubscription;
  @override
  void initState() {
    super.initState();

    items = new List.filled(1,ChatMessage("Date",
        "https://media.istockphoto.com/photos/brass-bell-at-the-door-to-the-old-style-picture-id471846154?k=6&m=471846154&s=612x612&w=0&h=uI65YP1GIh39aOGDpJlddC567C6UildrirboTGmXqQI=",
        "No One",
        "Time") ,growable: true);
    ChatMessagesReference.child('users').orderByKey().once().then((DataSnapshot dataSnapshot){

      var keys=dataSnapshot.value.keys;
      var data = dataSnapshot.value;
      for(var key in keys)
        {
          items.add(new ChatMessage(data[key]['date'], data[key]['image'], data[key]['name'], data[key]['time']));
        }
      setState(() {
        print('Length : ${items.length}');
      });

    });

    _onChatMessageAddedSubscription = ChatMessagesReference.onChildAdded.listen(_onChatMessageAdded);
  }

  @override
  void dispose() {
    _onChatMessageAddedSubscription.cancel();
    super.dispose();
  }

  void _onChatMessageAdded(Event event) {
    setState(() {
      items.add(new ChatMessage.fromSnapshot(event.snapshot));
    });
  }

  final _controller = ScrollController();

  @override
  Widget build(BuildContext context) {
    Timer(
      Duration(seconds: 1),
          () => _controller.jumpTo(_controller.position.maxScrollExtent),
    );

    return Scaffold(
      appBar: ChatDetailPageAppBar(),
      body: Stack(

        children: <Widget>[
          items.isEmpty ? Center(child: Text('Welcome to the online D-EYE Notifier')) :ListView.builder(
            controller: _controller,
            itemCount: items.length-1,
            shrinkWrap: true,
            padding: EdgeInsets.only(top: 10, bottom: 10),
//            physics: Scroll,
            itemBuilder: (context, index) {

              return ChatBubble(
                chatMessage: items[index],
              );
            },
          ),
        ],
      ),

    );
  }
}