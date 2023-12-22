# Schedule
.DRGファイルがGUI上で作成できる。  
SKDTools.py -- CUIで.DRGファイルを作成することができるモジュール。  
SKED_GUITool.py -- GUIで.DRGファイルを作成することができるプログラム。SKDTools.pyのfunctionを使用している。  

## Install (anaconda環境)
anacondaで仮想環境を作り、そこで動かす方法（pythonやモジュールのバージョン等が散らからない（仮想環境で閉じる）のでおすすめ）  
→ M1 Mac など architecture が異なると下の(3)でSolving environment: failed となってしまう。いくつか解決法はあるが、比較的簡単なのは module を都度インストールする方法（anaconda無しでもできる）。ただしpythonやmoduleのバージョンが合わない可能性があるので注意。おそらくpython 3.7以降であれば動く？（未確認）  
必要なmoduleは、numpy, matplotlib, astropy, astroquery, flet (fletはGUI用。普段使わないはずなのでinstall必須)。  

(0) anacondaのインストールは[こちら](https://www.anaconda.com/download)  
(1) 本ページに置いてあるファイルをダウンロードする。右上の Code → Download ZIP とすると良い。  
(2) 本プログラムを実行するための適当なディレクトリを作成し、ダウンロードしたファイルを置く。（antenna.sch はJVNのwebサイトなどから最新版を取得して使用すると良い。本ページのantenna.sch は、使用頻度が低いアンテナをコメントアウトしてある。）  
(3) ファイルを置いたディレクトリに移動し、  
`$ conda config --add channels conda-forge`  
でチャンネルを追加した後、  
`$ conda create --name <env> --file conda_requirements.txt`  
で仮想環境を作る。\<env> は環境名。例えばschedule。（必要なパッケージが conda_requirements.txt に記載してあるので、それを取ってくる。）  
(4) 環境を構築したら、 `$ conda activate <env>` で環境に入る。  
(5) 作成したディレクトリで （もしくはpathを通すなどして） `python SKED_GUITool.py` とすると起動する。  


（以下は必要に応じて）  
.skdファイルを作成したい時は、drgconv2020.out の実行ファイルを同じディレクトリに置く必要がある。  
相関用.xmlファイルを作成したいときは、mk_skd.py（穐本さん作成）を同じディレクトリに置く必要がある。
