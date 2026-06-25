2.2. Webサーバを公開する(NAT,NAPT)
====================================

| WCIルータとファイアウォール/ルータ等のセキュリティアプライアンスを接続し、NATおよびNAPTを利用してWCIアドレスを
| 拠点内のWebサーバ（443/TCP）に変換することで、拠点内のサーバをWCIネットワーク（IPv4）上に公開します。
| 同時に、外部公開を行わない閲覧用の拠点ネットワークを作成します。


2.2.1. 接続構成とネットワーク
------------------------------

**接続構成図** 

.. image:: ./images/webserver.png
   :scale: 30%

.. attention::
   | ※1,2　導入機種により接続ポートが異なります。詳しくは" :doc:`../preface/init` "の導入機種に応じたポート対応表をご確認下さい。
   | ※3  　ご契約拠点により、WCIアドレスおよびサブネットの割当範囲が異なります。別途ご確認下さい。本事例ではWCIアドレス割当範囲を ``100.65.21.0/26``、WCIルータのLANポートアドレスを ``100.65.21.1`` として記載します。


----

- **拠点ネットワークA** 

|   　本事例ではこのネットワークのみを外部に公開対象とし、Webサービスやアプリケーション(本事例では443/TCP) の提供を行います。  

- **拠点ネットワークB**  
  
|   　他拠点への公開は行わず、WCI-Portalや他拠点サービスへのアクセス用途に限定します。 

----

2.2.2. セキュリティアプライアンスについて
---------------------------------------------

| 基本的なNAT,NAPT機能を有する多くの機種で問題なくご利用いただける見込みです。
| 本事例では、アライドテレシス社のAT-ARX200S-GTX/AT-ARX200S-GT 及びFortinet社のFortiGate(FortiOS 7.2, 7.4)を例として設定方法を紹介します。

.. important::
   | AT-ARX200S-GTX/AT-ARX200S-GT は、アライドテレシスホールディングス株式会社の登録商標または商標です。
   | © Allied Telesis Holdings All rights reserved.
   | FortiGate および FortiOS GUI は Fortinet, Inc. の商標・著作物です。
   | © Fortinet, Inc. All rights reserved.


----


2.2.3.WCI-Portalの設定
-------------------------

.. tip::
   | WCI-Portalの詳細な操作方法については別紙 WCI-Portal 利用手順書 をご確認ください。

| **端末** から `WCI-Portal <https://portal.bbwci.net>`_ (`https://portal.bbwci.net`)にアクセスしログインします。
| 必要に応じて、WCIルータのLANポートに設定用端末を接続してアクセスして下さい。

サブネット管理
^^^^^^^^^^^^^^^^^^^^

以下の様に設定します。

.. image:: ./images/screen/n1.png
   :width: 900

.. csv-table::

   " **項目名** "," **項目内容** "
   " **サブネット名** ","sample_single_subnet"
   " **プレフィックス** ", "26"
   " **ネットワークアドレス** ", "100.65.21.0"

- **サブネット名** は任意の名称を設定できます。

このサブネットは後の手順でNATにより拠点ネットワークAのアドレスに対応付けられます。


----

接続
^^^^^^^^^

以下の様に設定します。

.. image:: ./images/screen/n2.png
   :width: 900


| 接続で指定するサブネットは **サブネットの登録** で作成した　``sample_single_subnet`` を指定してください。

----

フィルタ管理
^^^^^^^^^^^^^^^^

以下の様に設定します。

.. image:: ./images/screen/n3.png
   :width: 900


.. csv-table::

   " **項目名** "," **項目内容** "
   " **プロトコル** ","TCP"
   " **ポート** ", "443"

----


2.2.4. セキュリティアプライアンスの設定例
--------------------------------------------

.. dropdown:: AT-ARX200S-GTX/AT-ARX200S-GT 設定手順を表示する

   | NAT（ネットワークアドレス変換）とNAPT（ネットワークアドレスポート変換）機能を使用して、
   | WCIアドレス(IPv4)を拠点ネットワーク内の端末のアドレスへ変換する事で通信を実現します。
   

   **物理インタフェース構成**

   .. image:: ./images/screen/arx.png
      :scale: 30%

   .. rubric:: ・アドレス設定

   WCIアドレスは以下の様に定義されています。

   - 100.64.0.0 ～ 100.127.255.255 (100.64.0.0/10)

   .. important::
      | 本設定例に掲載されているコマンドは、設定がまったく行われていない本製品の初期状態から入力することを前提としています。
      | そのため、通常は ``erase startup-config`` を実行し、スタートアップコンフィグが存在しない状態で起動してから、設定を始めてください。
      | また、各コンフィグの詳細については、アライドテレシス社のコマンドリファレンスを参照してください。

   .. rubric:: ・デフォルト経路設定

   | デフォルト経路を既設ルーターのLAN側インターフェース（ ``100.65.21.1`` ）に向けて設定します。

   .. code-block:: none

      ip route 100.64.0.0/10 100.65.21.1

   .. rubric:: ・スパニングツリープロトコル（RSTP）無効化

   | LANポートにおいて初期状態で有効化されているスパニングツリープロトコル（RSTP）を無効化します。

   .. code-block:: none

      no spanning-tree rstp enable

   .. rubric:: ・WAN設定（eth1）

   | WANポート ``eth1`` にIPアドレスを設定します。
   | リミテッドローカルプロキシーARP機能を有効にし、サーバーのWCIアドレス宛てのARP要求に代理応答するよう設定します。

   .. code-block:: none

      interface eth1
       ip limited-local-proxy-arp
       ip address 100.65.21.2/26

   .. rubric:: ・ローカルプロキシーARP設定

   WANポートで有効にしたリミテッドローカルプロキシーARP機能の代理応答対象アドレスを指定します。
   
   .. code-block:: none

      local-proxy-arp 100.65.21.0/26

   .. rubric:: ・LAN設定（vlan10）

   | LAN側インターフェース ``LAN1,2`` 及び ``vlan10`` にIPアドレスを設定します。

   .. code-block:: none
      
      vlan database
       vlan 10
      !
      interface vlan10
       ip address 10.0.10.1/24
      !
      interface port1.0.1-1.0.2
      switchport
      switchport mode access
      switchport access vlan 10

   .. rubric:: ・LAN設定（vlan20）

   | LAN側インターフェース ``LAN3,4`` 及び ``vlan20`` にIPアドレスを設定します。

   .. code-block:: none
      
      vlan database
       vlan 20
      !
      interface vlan10
       ip address 172.16.10.1/24
      !
      interface port1.0.3-1.0.4
      switchport
      switchport mode access
      switchport access vlan 20


   .. rubric:: ・エンティティー定義

   | ファイアウォールやNATのルール作成時に使うエンティティー（通信主体）を定義します。

   拠点ネットワークを表すゾーン「private」を作成します。

   .. code-block:: none

      zone private
       network lan-b
        ip subnet 172.16.10.0/24
       network lan-a
        ip subnet 10.0.10.0/24
        host web
         ip address 10.0.10.10

   外部ネットワークを表すゾーン「public」を作成します。

   .. code-block:: none

      zone public
       network wan
        ip subnet 0.0.0.0/0 interface eth1
        host eth1
         ip address 100.65.21.2

   スタティックNAT用のWCIアドレスを表すゾーン「global」を作成します。

   .. code-block:: none

      zone global
       network wci
        ip subnet 100.65.21.0/26
        host web
         ip address 100.65.21.3

   .. rubric:: ・ファイアウォール設定

   | 外部からの通信を遮断しつつ、内部からの通信は自由に行えるようにするファイアウォール機能の設定を行います。

   - ``rule 10`` - WCIアドレス間の通信を許可します
   - ``rule 20`` - WCIアドレスから外部ネットワークへの通信を許可します
   - ``rule 30`` - 拠点ネットワークA内部同士の通信を許可します(任意)
   - ``rule 40`` - 外部ネットワークから拠点ネットワークAのWebサーバーへの通信を許可します（後述のNAT設定のrule20とペアで設定します）
   - ``rule 50`` - 拠点ネットワークB内部同士の通信を許可します(任意)
   - ``rule 60`` - 拠点ネットワークBから外部ネットワークへの通信を許可します
   - ``rule 70`` - 拠点ネットワークBからWCIアドレスへの通信を許可します

   .. code-block:: none

      firewall
       rule 10 permit any from global to global
       rule 20 permit any from global to public
       rule 30 permit any from private.lan-a to private.lan-a
       rule 40 permit https from public to private.lan-a.web
       rule 50 permit any from private.lan-b to private.lan-b
       rule 60 permit any from private.lan-b to public
       rule 70 permit any from private.lan-b to global
       protect

   .. rubric:: ・NAT設定

   | NAT機能の設定を行います。

   -  | ``rule 10`` - 拠点ネットワークB内部の端末がダイナミックENAT機能を使用できるようにします。
      | 変換後のアドレスとしてWAN側インターフェースの ``100.65.21.2`` を指定しています。
   - ``rule 20`` - WAN側で受信したWebサーバーのWCIアドレス宛てのHTTPパケットを、宛先をプライベートアドレスに変換して拠点ネットワークAのWebサーバーに転送します

   .. code-block:: none

      nat
       rule 10 masq any from private.lan-b to public with src public.wan.eth1
       rule 20 portfwd https from public to global.wci.web with dst private.lan-a.web
       enable

   .. rubric:: ・DNSフォワーディング設定

   | DNS機能の設定を行います。拠点ネットワーク内の端末がWCI上のドメインを解決できるように、
   | WCIルータのLAN側インターフェースのIPアドレスをDNSサーバーとして指定します。

   .. code-block:: none

      ip name-server 100.65.21.1
      ip domain-lookup
      ip dns forwarding

   以上で設定は完了です。

   .. rubric:: ・コンフィグ全体

   .. code-block:: none

      !
      no spanning-tree rstp enable
      !
      zone public
       network wan
        ip subnet 0.0.0.0/0 interface eth1
        host eth1
         ip address 100.65.21.2
      !
      zone private
       network lan-b
        ip subnet 172.16.10.0/24
       network lan-a
        ip subnet 10.0.10.0/24
        host web
         ip address 10.0.10.10
      !
      zone global
       network wci
        ip subnet 100.65.21.0/26
        host web
         ip address 100.65.21.3
      !
      firewall
       rule 10 permit any from global to global
       rule 20 permit any from global to public
       rule 30 permit any from private.lan-a to private.lan-a
       rule 40 permit https from public to private.lan-a.web
       rule 50 permit any from private.lan-b to private.lan-b
       rule 60 permit any from private.lan-b to public
       rule 70 permit any from private.lan-b to global
       protect
      !
      nat
       rule 10 masq any from private.lan-b to public with src public.wan.eth1
       rule 20 portfwd https from public to global.wci.web with dst private.lan-a.web
       enable
      !
      !
      ip name-server 100.65.21.1
      ip domain-lookup
      !
      !
      vlan database
       vlan 10,20 state enable
      !
      interface port1.0.1-1.0.2
       switchport
       switchport mode access
       switchport access vlan 10
      !
      interface port1.0.3-1.0.4
       switchport
       switchport mode access
       switchport access vlan 20
      !
      interface eth1
       ip limited-local-proxy-arp
       ip address 100.65.21.2/26
      !
      interface vlan10
       ip address 10.0.10.1/24
      !
      interface vlan20
       ip address 172.16.10.1/24
      !
      local-proxy-arp 100.65.21.0/26
      !
      ip route 100.64.0.0/10 100.65.21.1
      !
      ip dns forwarding
      !
      end





.. dropdown:: FortiGate(FortiOS 7.2,7.4) 設定手順を表示する

   | NAT（ネットワークアドレス変換）とNAPT（ネットワークアドレスポート変換）機能を使用して、
   | WCIアドレス(IPv4)を拠点ネットワーク内の端末のアドレスへ変換する事で通信を実現します。

   **物理インタフェース構成**

   .. image:: ./images/screen/fw.png
      :scale: 30%

   .. rubric:: ・アドレス設定

   WCIアドレスは以下の様に定義されています。

   - 100.64.0.0 ～ 100.127.255.255 (100.64.0.0/10)

   FortiGateのGUIダッシュボード画面より **[アドレス]** → **[新規作成]** からアドレスを以下の様に編集します。

   .. image:: ./images/screen/8.png
      :width: 800

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **IP/ネットマスク** “, “100.64.0.0 255.192.0.0”

   .. rubric:: ・スタティックルート設定

   **[スタティックルート]** → **[新規作成]** から新規スタティックルートを以下の様に編集します。

   .. image:: ./images/screen/9.png
      :width: 800

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **宛先(サブネット)** “, “100.64.0.0 255.192.0.0”
      “ **ゲートウェイアドレス** “, “100.65.21.1”
      “ **インタフェース** “, “wan1”

   .. rubric:: ・DNS設定

   **[DNS]** からDNS設定を以下の様に編集します。

   .. image:: ./images/screen/10.png
      :width: 800

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **DNSサーバ** “, “指定”
      “ **プライマリDNSサーバ** “, “100.65.21.1”
      “ **DNSプロトコル** “, “DNS(UDP/53)”

   .. rubric:: ・WAN設定

   | **[インタフェース]** から任意のインタフェースを選択して編集を行います。
   | 本事例では物理インタフェース ``wan1`` にWCIルータを接続する構成とするため、 ``wan1`` を選択します。

   .. image:: ./images/screen/11.png
      :width: 800

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **アドレッシングモード** “, “マニュアル”
      “ **IP/ネットマスク** “, “100.65.21.2/255.255.255.192”

   .. rubric:: ・LAN設定(拠点ネットワークA)

   | **[インタフェース]** から任意のインタフェースを選択して編集を行います。
   | 本事例では物理インタフェース ``internal1`` 配下に拠点ネットワークAを構成するため、 ``internal1`` を選択します。

   .. image:: ./images/screen/12.png
      :width: 800

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **アドレッシングモード** “, “マニュアル”
      “ **IP/ネットマスク** “, “10.0.10.1/255.255.255.0”

   .. rubric:: ・NAT設定(拠点ネットワークA)

   | **[バーチャルIP]** → **[新規作成]** から仮想IPを以下の様に編集します。

   .. image:: ./images/screen/13.png
      :width: 800

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **インタフェース** “, “wan1”
      “ **タイプ** “, “スタティックNAT”
      “ **外部IPアドレス/範囲** “, “100.65.21.3”
      “ **IPv4アドレス/範囲** “, “10.0.10.10”

   - **ポートフォワード** を有効化します。

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **プロトコル** “, “TCP”
      “ **ポートマッピングタイプ** “, “1対1”
      “ **外部サービスポート** “, “443”
      “ **IPv4ポートへマップ** “, “443”

   | 続いて、 **[IPプール]** → **[新規作成]** からダイナミックIPプールを以下の様に編集します。

   .. image:: ./images/screen/14.png
      :width: 800

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **タイプ** “, “オーバーロード”
      “ **外部IP範囲** “, “100.65.21.3-100.65.32.3”

   .. rubric:: ・ポリシー設定(拠点ネットワークA)

   | **[ファイアウォールポリシー]** → **[新規作成]** から以下の様にポリシーを作成します。

   .. image:: ./images/screen/15.png
      :width: 800

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **着信インタフェース** “, “wan1”
      “ **発信インタフェース** “, “internal1”
      “ **送信元** “, “WCI(アドレス設定で作成したもの)”
      “ **宛先** “, “VIP_WebServer(NAT設定-バーチャルIPで作成した物)”
      “ **サービス** “, “HTTPS”

   - **NAT** を有効化します。

   .. csv-table::

      “ **IPプール設定** “, “ダイナミックIPプールを使う”,”WebServer(NAT設定-IPプールで作成した物)”

   - 適切なセキュリティプロファイルを設定します

   | 接続を許可した他拠点から”100.65.21.3:443”でWebサーバにアクセスする事が可能となりました。
   | (ドメイン名,DNSレコードの追加・編集については、別紙 WCI-Portal 利用手順書 をご確認下さい。)
   | 続いて、拠点ネットワークBの設定を行います。

   .. tip::
      | 本事例では ``443/TCP`` を許可する設定ですが許可するプロトコル・ポートを変更することで任意のサービスを公開することが可能です。

   .. rubric:: ・LAN設定(拠点ネットワークB)

   | **[インタフェース]** から任意のインタフェースを選択して編集を行います。
   | 本事例では物理インタフェース ``internal2`` 配下に拠点ネットワークBを構成するため、 ``internal2`` を選択します。

   .. image:: ./images/screen/16.png
      :width: 800

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **アドレッシングモード** “, “マニュアル”
      “ **IP/ネットマスク** “, “172.16.10.1/255.255.255.0”

   .. rubric:: ・DNSサービス設定(拠点ネットワークB)

   | 拠点ネットワークBに対して、DNSプロキシの設定を行います。
   | 拠点ネットワークBの端末において ``internal2`` のアドレスをDNSサーバとして設定する事でDNSの通信をWCIルータに転送できます。
   |
   | **[DNSサーバ]** → **インタフェース上のDNSサービス** → **[新規作成]** からDNSサービスを以下の様に編集します。

   .. image:: ./images/screen/17.png
      :width: 800

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **インタフェース** “, “internal2”
      “ **モード** “, “システム設定DNSへ転送”

   ※ 拠点ネットワークAでも、DNSサーバをinternal1のアドレスとする時は同様にinternal1のDNSサービスを作成してください。

   .. rubric:: ・ポリシー設定(拠点ネットワークB)

   | **[ファイアウォールポリシー]** → **[新規作成]** から以下の様にポリシーを作成します。

   .. image:: ./images/screen/18.png
      :width: 800

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **着信インタフェース** “, “internal2”
      “ **発信インタフェース** “, “wan1”
      “ **送信元** “, “all”
      “ **宛先** “, “WCI(アドレス設定で作成したもの)”
      “ **サービス** “, “ALL”

   ※ **送信元** , **サービス** は利用用途に応じて適切に設定してください。

   - **NAT** を有効化します。

   .. csv-table::

      “ **項目名** “,” **項目内容** “
      “ **IPプール設定** “, “発信インタフェースアドレスを使用”

   - 適切なセキュリティプロファイルを設定します。

   | 拠点ネットワークBからWCI-Portalや他接続拠点で公開されているサービスへのアクセスが可能となりました。端末からの通信はNAPTにて、
   | ファイアウォールのアドレス 100.65.21.2 に変換されます。

