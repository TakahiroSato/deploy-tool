<template>
  <div id="main-pane">
    <hostList v-on:selectHost=selectHost :hosts=hosts />
    <div id="right-pane">
      <div style="margin-left: 50px; margin-top: 20px">
          <div>
            <h3>デプロイするディレクトリ</h3>
            <input type="text" v-model="deployDir" />
            <input type="button" value="参照" @click="openDialogForDeployDir()" />
          </div>
          <div>
            <textarea rows="10" cols="50" v-model="deployFiles"/>
          </div>
          <div>
            <h3>デプロイ先</h3>
            <input type="text" />
          </div>
          <div>
            <h3>バックアップ先</h3>
            <input type="text" v-model="backUpDir" />
            <input type="button" value="参照" @click="openDialogForBackUpDir()" />
          </div>
          <input type="button" value="test" @click="exec()" />
          <div style="position: absolute; bottom: 20px">
            <textarea id="output-window" disabled v-model="stdout" />
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
        connections: [],
        hosts: [],
        stdout: '',
        deployDir: '',
        deployFiles: '',
        backUpDir: ''
      }
    },
    methods: {
      selectHost: function (host) {
        // ToDo : implement
      },
      readFile: function () {
        const hostList = config.getHostList()
        this.connections = []
        this.connections = this.connections.concat(hostList)
        this.hosts = []
        this.hosts = this.connections.map(function (d) {
          return d.host
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
        var command = this.deployFiles
        exec(command, (error, stdout, stderr) => {
          if (error) {
            console.log(error)
          }
          const jschardet = require('jschardet')
          const iconv = require('iconv-lite')
          var buf = Buffer.alloc(stdout.length, stdout, 'binary')
          this.stdout = iconv.decode(buf, jschardet.detect(stdout).encoding)
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

  #output-window {
    width: 50em;
    height: 12em;
    background-color: black;
    color: white;
  }
</style>
