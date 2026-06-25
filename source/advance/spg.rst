3.3. SPGと連携する
=======================

| WCIルータとファイアウォール/ルータ等のセキュリティアプライアンスを接続する構成において、弊社のリモートデスクトップサービスである
| **SPG-Remote Medical** (以下SPG)を併用し、WCIネットワーク上でのリモートアクセス環境を実現します。
| 本事例では、SPG用ネットワークとWCIで利用する拠点ネットワークを分けて構成します。
| SPGの詳細な内容については `弊社のホームページ SPG-Remote Medical <https://bit-brain.jp/service/spg_medical>`_ をご確認ください。

----


3.3.1. 接続構成
-----------------

**接続構成図** 

.. image:: ./images/spg.png
   :scale: 25%

.. attention::
   - ※1,2 導入機種により接続ポートが異なります。詳しくは" :doc:`../preface/init` "の導入機種に応じたポート対応表をご確認下さい。
   - ※3,4 導入機種により接続ポートが異なります。SPGのご契約内容をご確認ください。
   - ※5 ご契約拠点により、WCIアドレスおよびサブネットの割当範囲が異なります。別途ご確認下さい。本事例ではWCIアドレス割当範囲を ``100.65.21.0/26``、WCIルータのLANポートアドレスを ``100.65.21.1`` として記載します。
   - ※6 SPGを使用する場合、ご利用できないWCIアドレスが存在します。詳細については後述します。

----

- **SPG Isolate Center** 

| 　　ビットブレインが管理運用するWCIネットワーク上のセキュリティクラウドです。

- **SPGネットワーク** 

| 　　SPGルータにより、SPG Isolate Centerからこのネットワーク内の端末へのSPG接続のみを自動で許可します。
| 　　ネットワークのアドレス範囲についてはSPGご契約時に指定いただいたサブネットを使用できます。本事例では、 ``192.168.1.0/24`` としています。 


- **拠点ネットワーク**  
  
| WCI-Portalや他拠点へのアクセス用途として設定を行います。本事例ではサービスの他拠点公開は行いません。 
| 他拠点に対してサービスを提供する場合は " :doc:`../standard/webserver` " をご確認ください。

----


.. tip::
   | SPGの利用にあたっては基本的に端末側の設定のみでご利用いただけます。端末の設定方法/SPGルータの接続設定・変更については、
   | SPGのご契約内容や利用手順書をご確認ください。


3.3.2. セキュリティアプライアンスについて
--------------------------------------------

| 基本的なNAT,NAPT機能を有する多くの機種で問題なくご利用いただける見込みです。
| 本事例では、アライドテレシス社のAT-ARX200S-GTX/AT-ARX200S-GT 及びFortinet社のFortiGate(FortiOS 7.2, 7.4)を例として設定方法を紹介します。

.. important::
   | AT-ARX200S-GTX/AT-ARX200S-GT は、アライドテレシスホールディングス株式会社の登録商標または商標です。
   | © Allied Telesis Holdings All rights reserved.
   | FortiGate および FortiOS GUI は Fortinet, Inc. の商標・著作物です。
   | © Fortinet, Inc. All rights reserved.



----

3.3.3. WCI-Portalの設定
---------------------------

.. tip::
   | WCI-Portalの詳細な操作方法については別紙 WCI-Portal 利用手順書 をご確認ください。

| **端末** から `WCI-Portal <https://portal.bbwci.net>`_ (`https://portal.bbwci.net`)にアクセスしログインします。
| 必要に応じて、WCIルータのLANポートに設定用端末を接続してアクセスして下さい。



サブネットの登録
^^^^^^^^^^^^^^^^^^
.. image:: ./images/screen/n9.png
   :width: 700

.. attention::

   | SPGをご契約の拠点の場合、上記画像の通り、システム予約によりSPG専用のサブネットが割り当てられています。
   | このサブネット範囲のアドレスをファイアウォール/ルータでハンドリングするとアドレスバッティングを引き起こす可能性が有りますのでご注意ください。

----

以下の様に拠点ネットワークのサブネットを設定します。

.. image:: ./images/screen/n5.png
   :width: 800

.. csv-table::

   " **項目名** "," **項目内容** "
   " **サブネット名** ","sample_subnet"
   " **プレフィックス** ", "29"
   " **ネットワークアドレス** ", "100.65.21.8"

- **サブネット名** は任意の名称を設定できます。

このサブネットが拠点ネットワークのアドレス帯となります。


----

接続
^^^^^

| SPG Isolate Centerとの接続はシステムにより自動的に生成されます。
| その他拠点との接続については別紙 `WCI Portal 利用手順書` をご確認ください。


----



フィルタ管理
^^^^^^^^^^^^^^^^

| 本事例では設定不要です。
| SPG Isolate CenterからSPGネットワーク内の端末へのSPG接続はシステムにより自動で許可されます。
|
| 拠点ネットワークで、サービスを公開する場合は" :doc:`../standard/webserver` "をご確認ください。

----


3.3.4. セキュリティアプライアンスの設定例
-------------------------------------------

.. dropdown:: AT-ARX200S-GTX/AT-ARX200S-GT 設定手順を表示する

   **物理インタフェース構成**

   .. image:: ./images/screen/spgarx.png
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

   .. code-block:: none

      interface eth1
       ip address 100.65.21.10/26

   .. rubric:: ・LAN設定（vlan1）

   | LAN側インターフェース ``vlan1`` にIPアドレスを設定します。

   .. code-block:: none
      
      interface vlan1
       ip address 172.16.10.1/24

   .. rubric:: ・エンティティー定義

   | ファイアウォールやNATのルール作成時に使うエンティティー（通信主体）を定義します。

   拠点ネットワークを表すゾーン「private」を作成します。

   .. code-block:: none

      zone private
       network lan
        ip subnet 172.16.10.0/24

   外部ネットワークを表すゾーン「public」を作成します。

   .. code-block:: none

      zone public
       network wan
        ip subnet 0.0.0.0/0 interface eth1
        host eth1
         ip address 100.65.21.10

   スタティックNAT用のWCIアドレスを表すゾーン「global」を作成します。

   .. code-block:: none

      zone global
       network wci
        ip subnet 100.65.21.0/26

   .. rubric:: ・ファイアウォール設定

   | 外部からの通信を遮断しつつ、内部からの通信は自由に行えるようにするファイアウォール機能の設定を行います。

   - ``rule 10`` - WCIアドレス間の通信を許可します
   - ``rule 20`` - WCIアドレスから外部ネットワークへの通信を許可します
   - ``rule 30`` - 拠点ネットワーク内部同士の通信を許可します(任意)
   - ``rule 40`` - 拠点ネットワークから外部ネットワークへの通信を許可します
   - ``rule 50`` - 拠点ネットワークからWCIアドレスへの通信を許可します

   .. code-block:: none

      firewall
       rule 10 permit any from global to global
       rule 20 permit any from global to public
       rule 30 permit any from private.lan to private.lan
       rule 40 permit any from private.lan to public
       rule 50 permit any from private.lan to global
       protect

   .. rubric:: ・NAT設定

   | NAT機能の設定を行います。

   -  | ``rule 10`` - 拠点ネットワークB内部の端末がダイナミックENAT機能を使用できるようにします。
      | 変換後のアドレスとしてWAN側インターフェースの ``100.65.21.10`` を指定しています。

   .. code-block:: none

      nat
       rule 10 masq any from private.lan to public with src public.wan.eth1
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
         ip address 100.65.21.10
      !
      zone private
       network lan
        ip subnet 172.16.10.0/24
      !
      zone global
       network wci
        ip subnet 100.65.21.0/26
      !
      firewall
       rule 10 permit any from global to global
       rule 20 permit any from global to public
       rule 30 permit any from private.lan to private.lan
       rule 40 permit any from private.lan to public
       rule 50 permit any from private.lan to global
       protect
      !
      nat
       rule 10 masq any from private.lan to public with src public.wan.eth1
       enable
      !
      !
      ip name-server 100.65.21.1
      ip domain-lookup
      !
      !
      !
      interface eth1
       ip address 100.65.21.10/26
      !
      interface vlan1
       ip address 172.16.10.1/24
      !
      !
      ip route 100.64.0.0/10 100.65.21.1
      !
      ip dns forwarding
      !
      end

.. dropdown:: FortiGate(FortiOS 7.4以降) 設定手順を表示する

   **物理インターフェース構成**

   .. image:: ./images/screen/fw2.png
      :scale: 30%

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

   .. image:: ./images/screen/2.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **宛先(サブネット)** ", "100.64.0.0 255.192.0.0"
      " **ゲートウェイアドレス** ", "100.65.21.1"
      " **インタフェース** ", "wan1"

   .. rubric:: ・DNS設定

   **[DNS]** からDNS設定を以下の様に編集します。

   .. image:: ./images/screen/3.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **DNSサーバ** ", "指定"
      " **プライマリDNSサーバ** ", "100.65.21.1"
      " **DNSプロトコル** ", "DNS(UDP/53)"

   .. rubric:: ・WAN設定

   | **[インタフェース]** から任意のインターフェースを選択して編集を行います。
   | 本事例では物理インターフェース ``wan1`` にWCIルータを接続する構成とするため、 ``wan1`` を選択します。

   .. image:: ./images/screen/22.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **アドレッシングモード** ", "マニュアル"
      " **IP/ネットマスク** ", "100.65.21.10/255.255.255.192"

   .. attention::
      本事例におけるSPGシステム予約サブネット範囲のIPアドレスは設定しないでください。

   .. rubric:: ・LAN設定(拠点ネットワーク)

   | **[インタフェース]** から任意のインターフェースを選択して編集を行います。
   | 本事例では物理インターフェース ``internal1`` 配下に拠点ネットワークBを構成するため、 ``internal1`` を選択します。

   .. image:: ./images/screen/23.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **アドレッシングモード** ", "マニュアル"
      " **IP/ネットマスク** ", "172.16.10.1/255.255.255.0"

   .. rubric:: ・DNSサービス設定(拠点ネットワーク)

   | 拠点ネットワークBに対して、DNSプロキシの設定を行います。
   | 拠点ネットワークBの端末において ``internal1`` のアドレスをDNSサーバとして設定する事でDNSの通信をWCIルータに転送できます。
   |
   | **[DNSサーバ]** → **インターフェース上のDNSサービス** → **[新規作成]** からDNSサービスを以下の様に編集します。

   .. image:: ./images/screen/25.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **インターフェース** ", "internal1"
      " **モード** ", "システム設定DNSへ転送"

   .. rubric:: ・ポリシー設定(拠点ネットワーク)

   | **[ファイアウォールポリシー]** → **[新規作成]** から以下の様にポリシーを作成します。

   .. image:: ./images/screen/24.png
      :width: 800

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **着信インターフェース** ", "internal1"
      " **発信インターフェース** ", "wan1"
      " **送信元** ", "all"
      " **宛先** ", "WCI(アドレス設定で作成したもの)"
      " **サービス** ", "ALL"

   ※ **送信元** , **サービス** は利用用途に応じて適切に設定してください。

   - **NAT** を有効化します。

   .. csv-table::

      " **項目名** "," **項目内容** "
      " **IPプール設定** ", "発信インタフェースアドレスを使用"

   - 適切なセキュリティプロファイルを設定します

   拠点ネットワークからWCI-Portalや他接続拠点で公開されているサービスへのアクセスが可能となりました。端末からの通信はNAPTにて、ファイアウォールのアドレス 100.65.21.10 に変換されます。