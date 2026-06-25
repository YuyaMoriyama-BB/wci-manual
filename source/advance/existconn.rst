3.2. 既設ネットワークをWCIと接続する
=======================================

| 既設のネットワークにWCIルータを接続し、NATおよびNAPTを利用してWCIアドレスを拠点内のWebサーバ（443/TCP）に変換することで、
| 既設ネットワーク内のサーバをWCIネットワーク上に公開します。

| " :doc:`../standard/webserver` " では全てのトラフィックをWCIルータに向ける形でしたが、本事例ではWCIネットワーク向けの通信は
| WCIルータにルーティングし、それ以外のトラフィックは既設のルーティングに従う設定とします。
| また、ファイアウォールにてWCIのドメインを含むDNSクエリを受信した際に、WCIのDNSサーバ(WCIルータ)にリダイレクトする様に設定します。
| これにより、既設ネットワークに大きな影響を与えずWCIネットワークに接続することが可能です。


3.2.1. 接続構成とネットワーク
------------------------------

**接続構成図**

.. image:: ./images/conn.png
   :scale: 25%

.. attention::
   | ※1,2　導入機種により接続ポートが異なります。詳しくは" :doc:`../preface/init` "の導入機種に応じたポート対応表をご確認下さい。
   | ※3  　ご契約拠点により、WCIアドレスおよびサブネットの割当範囲が異なります。別途ご確認下さい。本事例ではWCIアドレス割当範囲を ``100.65.21.0/26``、WCIルータのLANポートアドレスを ``100.65.21.1`` として記載します。


----

- **既設ネットワーク**

このネットワークのみを他拠点に公開対象とし、Webサービスやアプリケーション (本事例では443/TCP) の提供を行います。また、端末からWCI-Portalや他拠点サービスへのアクセスを行えるように設定を行います。


----

3.2.2. セキュリティアプライアンスについて
---------------------------------------------

| 基本的なNAT,NAPT機能を有する多くの機種で問題なくご利用いただける見込みです。
| 本事例では、アライドテレシス社のAT-ARX200S-GTX/AT-ARX200S-GT 及びFortinet社のFortiGate(FortiOS 7.2, 7.4)を例として設定方法を紹介します。

.. important::
   | AT-ARX200S-GTX/AT-ARX200S-GT は、アライドテレシスホールディングス株式会社の登録商標または商標です。
   | © Allied Telesis Holdings All rights reserved.
   | FortiGate および FortiOS GUI は Fortinet, Inc. の商標・著作物です。
   | © Fortinet, Inc. All rights reserved.


----


3.2.3.WCI-Portalの設定
-------------------------

.. tip::
   | WCI-Portalの詳細な操作方法については別紙 WCI-Portal 利用手順書 をご確認ください。

| **端末** から `WCI-Portal <https://portal.bbwci.net>`_ (`https://portal.bbwci.net`)にアクセスしログインします。
| 必要に応じて、WCIルータのLANポートに設定用端末を接続してアクセスして下さい。

サブネット管理
^^^^^^^^^^^^^^^^^^^^

以下の様に設定します。

.. image:: ./images/screen/n5.png
   :scale: 50%

.. csv-table::

   " **項目名** "," **項目内容** "
   " **サブネット名** ","sample_single_subnet"
   " **プレフィックス** ", "26"
   " **ネットワークアドレス** ", "100.65.21.0"

- **サブネット名** は任意の名称を設定できます。

このサブネットは後の手順でNATにより既設ネットワークAのアドレスに対応付けられます。


----

接続
^^^^^^^^^

以下の様に設定します。

.. image:: ./images/screen/n6.png
   :width: 900

| 接続で指定するサブネットは **サブネットの登録** で作成した　``sample_single_subnet`` を指定してください。


----

フィルタ管理
^^^^^^^^^^^^^^^^

以下の様に設定します。

.. image:: ./images/screen/n7.png
   :width: 900

.. csv-table::

   " **項目名** "," **項目内容** "
   " **プロトコル** ","TCP"
   " **ポート** ", "443"


----


3.2.4. セキュリティアプライアンスの設定例
--------------------------------------------

.. dropdown:: AT-ARX200S-GTX/AT-ARX200S-GT 設定手順を表示する

   **物理インタフェース構成**

   .. image:: ./images/screen/existconnarx.png
      :scale: 30%

   .. rubric:: ・アドレス設定

   WCIアドレスは以下の様に定義されています。

   - 100.64.0.0 ～ 100.127.255.255 (100.64.0.0/10)

   .. important::
      | 本設定例に掲載されているコマンドは、設定がまったく行われていない本製品の初期状態から入力することを前提としています。
      | そのため、通常は ``erase startup-config`` を実行し、スタートアップコンフィグが存在しない状態で起動してから、設定を始めてください。
      | また、各コンフィグの詳細については、アライドテレシス社のコマンドリファレンスを参照してください。

   .. important::
      | 本設定例では、AT-ARX200S-GTX/AT-ARX200S-GT の物理ポートLAN4を既設WAN向けに、物理ポートETH1をWCI向けとして設定しています。
      | また、既設WANの上位機器からDHCPでIPアドレス及びDNSサーバの情報を取得することを前提としています。
      | 既設のネットワーク構成に応じて、適宜設定内容を変更してください。

   .. rubric:: ・経路設定

   | WCI向けの通信経路をWCIルーターのLAN側インターフェース（ ``100.65.21.1`` ）に向けて設定し
   | デフォルトルートを既設WANの上位機器に向けて設定します。

   .. code-block:: none

      ip route 0.0.0.0/0 port1.0.4
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

   .. rubric:: ・WAN設定（port1.0.4）

   | ポート ``port1.0.4`` にIPアドレスを設定します。no switchport コマンドによりルータポートとして機能します

   .. code-block:: none

      interface port1.0.4
       no switchport
       ip address dhcp

   .. rubric:: ・LAN設定（vlan1）

   | LAN側インターフェース ``vlan1`` にIPアドレスを設定します。

   .. code-block:: none
      
      interface vlan1
       ip address 172.16.1.1/24

   .. rubric:: ・エンティティー定義

   | ファイアウォールやNATのルール作成時に使うエンティティー（通信主体）を定義します。

   拠点ネットワークを表すゾーン「private」を作成します。

   .. code-block:: none

      zone private
       network lan
        ip subnet 172.16.1.0/24
        host web
         ip address 172.16.1.100

   外部ネットワークを表すゾーン「public」を作成します。

   .. code-block:: none

      zone public
       network wan2
        ip subnet 100.64.0.0/10 interface eth1
        host eth1
         ip address 100.65.21.2
       network wan1
        ip subnet 0.0.0.0/0 interface port1.0.4
        host port4
         ip address dynamic interface port1.0.4

   スタティックNAT用のWCIアドレスを表すゾーン「global」を作成します。

   .. code-block:: none

      zone global
       network wci
        ip subnet 100.65.21.0/26

   .. rubric:: ・ファイアウォール設定

   | 外部からの通信を遮断しつつ、内部からの通信は自由に行えるようにするファイアウォール機能の設定を行います。

   - ``rule 10`` - WCIアドレス間の通信を許可します
   - ``rule 20`` - WCIアドレスから外部ネットワークへの通信を許可します
   - ``rule 30`` - 既設WANの上位機器と本ルータ間の通信を許可します
   - ``rule 40`` - 拠点ネットワーク内部同士の通信を許可します(任意)
   - ``rule 50`` - 拠点ネットワークから外部ネットワークへの通信を許可します
   - ``rule 60`` - 拠点ネットワークからWCIアドレスへの通信を許可します
   - ``rule 70`` - 他のWCIネットワークから既設ネットワークのWebサーバーへの通信を許可します（後述のNAT設定のrule30とペアで設定します）

   .. code-block:: none

      firewall
       rule 10 permit any from global to global
       rule 20 permit any from global to public
       rule 30 permit any from public.wan1 to public.wan1
       rule 40 permit any from private.lan to private.lan
       rule 50 permit any from private.lan to public
       rule 60 permit any from private.lan to global
       rule 70 permit https from public.wan2 to private.lan.web
       protect
      !

   .. rubric:: ・NAT設定

   | NAT機能の設定を行います。

   -  | ``rule 10`` - 既設ネットワーク内部の端末がWCI向けの通信の際にダイナミックENAT機能を使用できるようにします。
      | 変換後のアドレスとしてWAN側インターフェースの ``100.65.21.10`` を指定しています。

   -  | ``rule 20`` - 既設ネットワーク内部の端末が既設WAN向けの通信の際にダイナミックENAT機能を使用できるようにします。
      | 変換後のアドレスとしてWAN側インターフェースの DHCPアドレスを指定しています。

   -  | ``rule 30`` - WAN側で受信したWebサーバーのWCIアドレス宛てのHTTPパケットを、宛先をプライベートアドレスに変換して
      | 既設ネットワークのWebサーバーに転送します

   .. code-block:: none

      nat
       rule 10 masq any from private.lan to public.wan2 with src public.wan2.eth1
       rule 20 masq any from private.lan to public.wan1 with src public.wan1.port4
       rule 30 portfwd https from public to global.wci.web with dst private.lan.web
       enable

   .. rubric:: ・DNSフォワーディング設定

   | DNS機能の設定を行います。拠点ネットワーク内の端末がWCI上のドメインを解決できるように、
   | WCIルータのLAN側インターフェースのIPアドレスをDNSサーバーとして指定します。
   | WCI上のドメイン は ``bbwci.net`` で定義されるため、DNSサフィックスとして ``bbwci.net`` を指定します。
   | これにより、``bbwci.net`` のドメインを含むDNSクエリはWCIルータに転送され、それ以外のクエリは既設WANの上位機器に転送されます。

   .. code-block:: none

      ip name-server 100.65.21.1 suffix-list wci
      ip domain-lookup
      ip dns forwarding
      ip dns forwarding domain-list wci
       domain bbwci.net

   以上で設定は完了です。

   .. rubric:: ・コンフィグ全体

   .. code-block:: none

      !
      zone public
       network wan2
        ip subnet 100.64.0.0/10 interface eth1
        host eth1
         ip address 100.65.21.2
       network wan1
        ip subnet 0.0.0.0/0 interface port1.0.4
        host port4
         ip address dynamic interface port1.0.4
      !
      zone private
       network lan
        ip subnet 172.16.1.0/24
        host web
         ip address 172.16.1.100
      !
      zone global
       network wci
        ip subnet 100.65.21.0/26
      !
      firewall
       rule 10 permit any from global to global
       rule 20 permit any from global to public
       rule 30 permit any from public.wan1 to public.wan1
       rule 40 permit any from private.lan to private.lan
       rule 50 permit any from private.lan to public
       rule 60 permit any from private.lan to global
       rule 70 permit https from public to private.lan.web
       protect
      !
      nat
       rule 10 masq any from private.lan to public.wan2 with src public.wan2.eth1
       rule 20 masq any from private.lan to public.wan1 with src public.wan1.port4
       rule 30 portfwd https from public to global.wci.web with dst private.lan.web
       enable
      !
      !
      ip name-server 100.65.21.1 suffix-list wci
      ip domain-lookup
      !
      !
      !
      interface port1.0.4
       no switchport
       ip address dhcp
      !
      interface eth1
       ip limited-local-proxy-arp
       ip address 100.65.21.2/26
      !
      interface vlan1
       ip address 172.16.1.1/24 
      !
      local-proxy-arp 100.65.21.0/26
      !
      ip route 0.0.0.0/0 port1.0.4
      ip route 100.64.0.0/10 100.65.21.1
      !
      ip dns forwarding
      ip dns forwarding domain-list wci
       domain bbwci.net
      !
      !
      end

.. dropdown:: FortiGate(FortiOS 7.2,7.4) 設定手順を表示する

   | NAT（ネットワークアドレス変換）とNAPT（ネットワークアドレスポート変換）機能を使用して、
   | WCIアドレス(IPv4)を拠点ネットワーク内の端末のアドレスへ変換する事で通信を実現します。

   **物理インタフェース構成**

   .. image:: ./images/screen/connfw.png
      :width: 900


   .. rubric:: ・アドレス設定

   WCIアドレスは以下の様に定義されています。

   - 100.64.0.0 ～ 100.127.255.255 (100.64.0.0/10)

   FortiGateのGUIダッシュボード画面より **[アドレス]** → **[新規作成]** からアドレスを以下の様に編集します。

   .. image:: ./images/screen/1.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **IP/ネットマスク** ", "100.64.0.0 255.192.0.0"


   .. rubric:: ・スタティックルート設定

   **[スタティックルート]** → **[新規作成]** から新規スタティックルートを以下の様に編集します。

   .. image:: ./images/screen/2.5.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **宛先(サブネット)** ", "100.64.0.0 255.192.0.0"
      " **ゲートウェイアドレス** ", "100.65.21.1"
      " **インタフェース** ", "wan2"


   .. rubric:: ・DNS設定

   **[DNSサーバ]→[DNSデータベース]** の **[新規作成]** をします。

   .. image:: ./images/screen/13.png
      :width: 800

   以下のように設定します。

   .. image:: ./images/screen/14.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **DNSゾーン** ", "WCI"
      " **ドメイン名** ", "bbwci.net"
      " **DNSフォワーダ** ", "100.65.21.1"

   **[DNSゾーン]** は任意の名称を設定できます。

   続いて、CLI設定より送信元 IP を設定します。

   .. code-block:: shell

      config system dns-database
         edit "WCI"
           set domain "bbwci.net"
           set forwarder "100.65.21.65"
         next
      end


   続いて、[インターフェース上のDNSサービス]の[新規作成]をします。
   以下の様に設定します。

   .. image:: ./images/screen/15.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **インタフェース** ", "lan"
      " **モード** ", "再帰的"


   この設定により、lanポートのアドレスがDNSプロキシとして働くようになり
   bbwci.netのドメインを含むDNSクエリがWCIルータに、その他のクエリに関しては既設のプライマリDNSに転送されるようになります。


   .. rubric:: ・WAN設定

   | **[インタフェース]** から任意のインタフェースを選択して編集を行います。
   | 本事例では物理インタフェース ``wan2`` にWCIルータを接続する構成とするため、 ``wan2`` を選択します。

   .. image:: ./images/screen/16.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **アドレッシングモード** ", "マニュアル"
      " **IP/ネットマスク** ", "100.65.21.2/255.255.255.192"


   .. rubric:: ・LAN設定(既設ネットワーク)

   | **[インタフェース]** から任意のインタフェースを選択して編集を行います。
   | 本事例では既設ネットワークとして物理インターフェース" lan"を設定しています。

   .. image:: ./images/screen/17.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **アドレッシングモード** ", "マニュアル"
      " **IP/ネットマスク** ", "172.16.1.1/255.255.255.0"


   .. rubric:: ・NAT設定(既設ネットワーク)

   | **[バーチャルIP]** → **[新規作成]** から仮想IPを以下の様に編集します。

   .. image:: ./images/screen/18.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **インタフェース** ", "wan2"
      " **タイプ** ", "スタティックNAT"
      " **外部IPアドレス/範囲** ", "100.65.21.3"
      " **IPv4アドレス/範囲** ", "172.16.1.100"

   - **ポートフォワード** を有効化します。

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **プロトコル** ", "TCP"
      " **ポートマッピングタイプ** ", "1対1"
      " **外部サービスポート** ", "443"
      " **IPv4ポートへマップ** ", "443"

   | 続いて、 **[IPプール]** → **[新規作成]** からダイナミックIPプールを以下の様に編集します。

   .. image:: ./images/screen/19.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **タイプ** ", "オーバーロード"
      " **外部IP範囲** ", "100.65.21.3-100.65.32.3"

   .. rubric:: ・ポリシー設定(既設ネットワーク)

   | in側のポリシーを作成します。
   | **[ファイアウォールポリシー]** → **[新規作成]** から以下の様にポリシーを作成します。

   .. image:: ./images/screen/20.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **着信インタフェース** ", "wan2"
      " **発信インタフェース** ", "lan"
      " **送信元** ", "WCI(アドレス設定で作成したもの)"
      " **宛先** ", "VIP_WebServer(NAT設定-バーチャルIPで作成した物)"
      " **サービス** ", "HTTPS"

   - **NAT** を有効化します。

   .. csv-table::

      " **IPプール設定** ", "ダイナミックIPプールを使う","WebServer(NAT設定-IPプールで作成した物)"

   - 適切なセキュリティプロファイルを設定します

   | 接続を許可した他拠点から"100.65.21.3:443"でWebサーバにアクセスする事が可能となりました。
   | (ドメイン名,DNSレコードの追加・編集については、別紙 WCI-Portal 利用手順書 をご確認下さい。)

   .. tip::
      | 本事例では ``443/TCP`` を許可する設定ですが許可するプロトコル・ポートを変更することで任意のサービスを公開することが可能です。

   | 続いてout側のポリシーを作成します。
   | **[ファイアウォールポリシー]** → **[新規作成]** から以下の様にポリシーを作成します。

   .. image:: ./images/screen/21.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **着信インタフェース** ", "lan"
      " **発信インタフェース** ", "wan2"
      " **送信元** ", "all"
      " **宛先** ", "WCI(アドレス設定で作成したもの)"
      " **サービス** ", "HTTPS"

   - **送信元 サービス** は利用用途に応じて適切に設定してください。

   - **NAT** を有効化します。

   .. csv-table::

      " **IPプール設定** ", "発信インタフェースアドレスを使用"

   - 適切なセキュリティプロファイルを設定します

   これで、既設ネットワークからWCI-Portalや他接続拠点で公開されているサービスへのアクセスが可能となります。端末からの通信はNAPTにて、ファイアウォールのアドレス 100.65.21.2 に変換されます。
