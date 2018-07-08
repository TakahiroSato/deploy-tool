<template>
  <div id="main-pane">
    <hostList v-on:selectHost=selectHost :hosts=hosts />
    <div id="right-pane">
      <div style="margin-left: 50px; margin-top: 20px">
          <div>
            <h3>デプロイするディレクトリ</h3>
            <input type="text" v-model="deployDir" style="width:30em"/>
            <input type="button" value="参照" @click="openDialogForDeployDir()" />
          </div>
          <div>
            <textarea rows="10" cols="70" v-model="deployFiles" disabled/>
          </div>
          <div>
            <h3>デプロイ先</h3>
            <input type="text" v-model="remoteDir" style="width:30em"/>
          </div>
          <div>
            <h3>バックアップ先</h3>
            <input type="text" v-model="backUpDir" style="width:30em"/>
            <input type="button" value="参照" @click="openDialogForBackUpDir()" />
          </div>
          <input type="button" value="deploy" @click="exec()" />
          <div>
            <textarea id="output-window" v-model="stdout" disabled/>
          </div>
      </div>
    </div>
  </div>
</template>

<script>
  import hostList from '../hostList'
  const {dialog} = require('electron').remote
  const config = require('config').default
  export default {
    name: 'deploy-page',
    components: {
      hostList
    },
    data: function () {
      return {
        selectedSettingName: '',
        connections: [],
        hosts: [],
        stdout: '',
        deployDir: '',
        deployFiles: '',
        remoteDir: '',
        backUpDir: ''
      }
    },
    methods: {
      selectHost: function (settingName) {
        const setting = config.getHostList().filter(function (v, i) {
          return v.settingName === settingName
        })
        this.selectedSettingName = setting[0].settingName
        this.backUpDir = setting[0].backupPath
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
      openDialogForDeployDir: function () {
        dialog.showOpenDialog(
          {
            properties: ['openDirectory'],
            title: 'select deploy directory'
          }, (dirName) => {
            if (dirName) {
              this.deployDir = dirName
              this.deployFiles = this.getFileNames(dirName).map(
                f => dirName.toString() + '\\' + f).join('\n')
            }
          })
      },
      openDialogForBackUpDir: function () {
        dialog.showOpenDialog(
          {
            properties: ['openDirectory'],
            title: 'select backup directory'
          }, (dirName) => {
            if (dirName) {
              this.backUpDir = dirName
            }
          })
      },
      exec: function () {
        const exec = require('child_process').exec
        var command = 'cd src/py & pipenv run fab setHost:' +
          this.selectedSettingName + ',' +
          this.deployDir + ',' +
          this.remoteDir + ',' +
          this.backUpDir + ' deploy'
        exec(command, (error, stdout, stderr) => {
          if (error) {
            console.log(error)
          }
          const jschardet = require('jschardet')
          const iconv = require('iconv-lite')
          var buf = Buffer.alloc(stdout.length, stdout, 'binary')
          this.stdout = iconv.decode(buf, jschardet.detect(stdout).encoding)
        })
      },
      getFileNames: function (dir) {
        return require('fs-readdir-recursive')(dir.toString())
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

  #output-window {
    width: 50em;
    height: 12em;
    background-color: black;
    color: white;
  }
</style>
