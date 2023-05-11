import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class ChatDetailPageAppBar extends StatelessWidget implements PreferredSizeWidget{

  @override
  Widget build(BuildContext context) {
    return AppBar(
      elevation: 0,
      automaticallyImplyLeading: false,
      backgroundColor: Colors.white,
      flexibleSpace: SafeArea(
        child: Container(
          padding: EdgeInsets.only(right: 16),
          child: Row(
            children: <Widget>[

              SizedBox(width: 15,),
              CircleAvatar(
                backgroundImage: AssetImage("images/userImage2.jpg"),
                maxRadius: 20,
              ),
              SizedBox(width: 12,),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    Text("DoorBell Notifier",style: TextStyle(fontWeight: FontWeight.w600),),
                    SizedBox(height: 6,),
                    Text("Online",style: TextStyle(color: Colors.green,fontSize: 12),),
                  ],
                ),
              ),
//              IconButton(
//                onPressed: (){
//
//                },
//                icon: Icon(Icons.refresh,color: Colors.green,),
//              ),
//              SizedBox(width: 12,),
//              Icon(Icons.settings_power,color: Colors.redAccent,),
            ],
          ),
        ),
      ),
    );
  }

  @override
  // TODO: implement preferredSize
  Size get preferredSize => Size.fromHeight(kToolbarHeight);
}