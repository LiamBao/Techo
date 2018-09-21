
install rvm / ruby 
sudo gem install -n /usr/local/bin cocoapods
如果安装了多个Xcode使用下面的命令选择（一般需要选择最近的Xcode版本）
sudo xcode-select -switch /Applications/Xcode.app/Contents/Developer
pod setup
vi to Podfile :
     pod 'package'