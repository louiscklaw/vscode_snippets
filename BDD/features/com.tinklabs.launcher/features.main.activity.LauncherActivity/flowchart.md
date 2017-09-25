# feature/features.main.activity.LauncherActivity flowchart

#### flow of activation

```mermaid
graph TB

subgraph_1st_time_activation --> v_launcher(launcher)
v_launcher--tap_home-->wv_home
v_launcher--tap_App-->?_App
v_launcher--tap_City_Guide-->wv_City_Guide
v_launcher--tap_Shop-->wv_Shop
v_launcher--tap_ticket-->wv_Ticket
v_launcher--tap_Call-->act_handy_phone
```

- subgraph 1st time activation
```mermaid
graph TB
subgraph 1st_time_activation
  tstart(tutorial_start_here)
    --> t1[Tap_this_show_the_hostel_details]
  t1 -- tap --> t2[Tap_on_this_icon_to_open_the_side_bar]
  t2 -- tap --> t3[Scroll_down_to_explore_all_the_main_features_of_handy]
  t3 -- tap --> t4(Shop_for_discounted_souvenirs)
  t4 -- tap --> t5(Tours_and_tickets_to_major_attractions)
  t5 -- tap --> tTicket(wv_Tickets)
  tTicket -- tap back on wv_Tickets --> wv_launcher_lobby(launcher_lobby)
  wv_launcher_lobby-->tdone(tutorial_done)
end
```
- subgraph City_Guide
```mermaid
graph TB
wv_City_Guide--tap_CITY_GUIDE--> wv_City_Guide
wv_City_Guide--tap_SHOP-->  wv_SHOP
wv_City_Guide--tap_EAT--> wv_EAT
wv_City_Guide--tap_DO--> wv_DO
wv_City_Guide--tap_BEAUTY--> wv_BEAUTY
wv_City_Guide--tap_KIDS--> wv_KITS
```

- subgraph shop
```mermaid
graph TB
wv_Shop--tap_IN_ROOM_SHOPPING-->wv_IN_ROOM_SHOPPING
wv_Shop--tap_健康保健-->wv_健康保健
wv_Shop--tap_時尚電子-->wv_時尚電子
wv_Shop--tap_休間食品-->wv_休間食品
wv_Shop--tap_健康美容-->wv_健康美容
```


- subgraph ticketing
```mermaid
graph TB

wv_Ticket--tap_btn_ticket-->wv_Ticket
wv_Ticket--tap_btn_Order-->wv_Order
wv_Order--tap_btn_Explore-->wv_Ticket
wv_Ticket--tap_btn_Help-->wv_Help
wv_Help--tap_FAQ-->wv_FAQ
wv_Help--tap_about_ticketing-->wv_about_ticketing
wv_Ticket--history_back-->Shop
wv_Ticket--history_back-->CITY_GUIDE
wv_Ticket--history_back-->Apps
```


- subgraph handy_phone
```mermaid
graph TB
handy_phone-->phone_book
handy_phone-->dialer
handy_phone-->call_history
handy_phone-->contacts
```

#### steps to be filled

```sequence
1 -> 2: hehe
2 -> 1: haha
```
