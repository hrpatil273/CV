import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/cupertino.dart';

import '../chat_detail_page.dart';

class ChatMessage{
  String name='',date='',image='',time='';
  ChatMessage(this.date,this.image,this.name,this.time);

  ChatMessage.map(dynamic obj)
  {
    this.name =obj['_name'];
    this.date =obj['_date'];
    this.image =obj['_image'];
    this.time =obj['_time'];
  }

  String get _name => name;
  String get _date => date;
  String get _image => image;
  String get _time => time;

  ChatMessage.fromSnapshot(DataSnapshot snapshot) {
//    _name = snapshot.key;
    name = snapshot.value['_name'];
    date = snapshot.value['_date'];
    image = snapshot.value['_image'];
    time = snapshot.value['_time'];
  }
}