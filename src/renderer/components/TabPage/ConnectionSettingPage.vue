<template>
  <div id="main-pane">
    <hostList v-on:selectHost=changeSetting :hosts=hosts />
    <div id="right-pane">
      <div style="margin-left: 50px; margin-top: 20px">
          <div style="margin-top: 20px">
            <h3>設定名</h3>
            <input type="text" v-model="inputSettingName" placeholder="name">
          </div>
          <div style="margin-top: 20px">
            <h3>接続先</h3>
            <input type="text" v-model="inputHost" placeholder="host or ip">
          </div>
          <div style="margin-top: 20px">
            <h3>ユーザ名</h3>
            <input type="text" v-model="inputUserName" placeholder="user name">
          </div>
          <div style="margin-top: 20px">
            <h3>秘密鍵</h3>
            <input type="text" v-model="inputSecretKeyPath" placeholder="secret key path">
            <input type="button" value="参照" @click="openDialogForFile">
          </div>
          <div style="margin-top: 20px">
            <h3>パスワード</h3>
            <input type="text" v-model="inputPassword" placeholder="password">
          </div>
          <div style="margin-top: 20px">
            <h3>バックアップ先</h3>
            <input type="text" v-model="inputBackUpPath" placeholder="backup path">
            <input type="button" value="参照" @click="openDialogForDir">
          </div>
          <div style="margin-top: 20px">
            <input id="save" type="submit" value="保存" @click="save()">
          </div>
      </div>
    </div>
  </div>
</template>

<script>
  import hostList from '../hostList'
  const {dialog} = require('electron').remote
  const config = require('config').default
  const connectionsFilePath = config.connectionsFilePath
  export default {
    name: 'connection-setting-page',
    components: {
      hostList
    },
    data: function () {
      return {
        inputSettingName: '',
        inputHost: '',
        inputUserName: '',
        inputSecretKeyPath: '',
        inputPassword: '',
        inputBackUpPath: '',
        connections: [],
        hosts: []
      }
    },
    methods: {
      save: function () {
        var fs = require('fs')
        this.connections.some(function (v, i) {
          if (v.settingName === this.inputSettingName) this.connections.splice(i, 1)
        }.bind(this))
        this.connections.push({
          settingName: this.inputSettingName,
          host: this.inputHost,
          userName: this.inputUserName,
          secretKey: this.inputSecretKeyPath,
          password: this.inputPassword,
          backupPath: this.inputBackUpPath
        })
        fs.writeFileSync(connectionsFilePath,
          JSON.stringify(this.connections, null, ''), 'utf-8', (err) => {
            if (err) {
              console.log(err)
              throw err
            }
          })
        this.readFile()
      },
      readFile: function () {
        const hostList = config.getHostList()
        this.connections = []
        this.connections = this.connections.concat(hostList)
        this.hosts = []
        this.hosts = this.connections.map(function (d) {
          return d.settingName
        })
      },
      changeSetting: function (settingName) {
        var setting = this.connections.filter(function (v, i) {
          if (v.settingName === settingName) return true
        })
        setting = setting[0]
        this.inputSettingName = setting.settingName
        this.inputHost = setting.host
        this.inputUserName = setting.userName
        this.inputSecretKeyPath = setting.secretKey
        this.inputPassword = setting.password
        this.inputBackUpPath = setting.backupPath
      },
      openDialogForFile: function () {
        dialog.showOpenDialog(
          {
            properties: ['openFile'],
            title: 'select ssh secretkey file'
          }, (fileName) => {
            if (fileName) {
              this.inputSecretKeyPath = fileName
            }
          })
      },
      openDialogForDir: function () {
        dialog.showOpenDialog(
          {
            properties: ['openDirectory'],
            title: 'select backup directory'
          }, (dirName) => {
            if (dirName) {
              this.inputBackUpPath = dirName
            }
          })
      }
    },
    mounted: function () {
      this.readFile()
    }
  }
</script>

<style>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body { font-family: 'Source Sans Pro', sans-serif; }

  #main-pane {
    height: inherit;
    margin: 0px 15px 10px 0px;
    border: 2px solid #999999;
  }

  #right-pane {
    height: inherit;
    display: inline-block;
      float:left;
  }

  #save{
    padding: 0.5em 1em;
    text-decoration: none;
    background: #7FB6F5;
  }
</style>
