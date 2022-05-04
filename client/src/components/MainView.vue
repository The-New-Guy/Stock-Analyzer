<!-- eslint-disable max-len -->
<template>
  <div class="container">
    <div class="row">
      <div class="bg-grey col-sm-10">
        <h1>Stock Analyzer</h1>
        <hr><br><br>

        <!-- Date Range Picker -->

        <form class="shadow-md rounded px-8 pt-6 pb-8" @submit.prevent>
          <div class="mb-4">
            <span class="block text-gray-600 text-sm text-left font-weight-bold mb-2">Select Range</span>
            <br>
            <v-date-picker
              v-model="dateRange"
              mode="date"
              :masks="masks"
              is-range
              is-inline
              is-dark
              color="blue"
            >
              <template v-slot="{ inputEvents, isDragging }">
                <div class="d-flex sm:flex-row justify-content-left">
                  <div class="relative flex-grow">
                    <svg
                      class="text-gray-600 w-4 h-full mx-2 absolute pointer-events-none"
                      fill="none"
                      width=40px
                      height=40px
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                    <input
                      class="flex-grow pl-8 pr-2 py-1 bg-gray-100 border rounded w-full"
                      :class="isDragging ? 'text-gray-600' : 'text-gray-900'"
                      :value="dateRange.start"
                      v-on="inputEvents.start"
                    />
                  </div>
                  <span class="flex-shrink-0 m-2">
                    <svg
                      class="w-4 h-4 stroke-current text-gray-600"
                      width=40px
                      height=40px
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M14 5l7 7m0 0l-7 7m7-7H3"
                      />
                    </svg>
                  </span>
                  <div class="relative flex-grow">
                    <svg
                      class="text-gray-600 w-4 h-full mx-2 absolute pointer-events-none"
                      fill="none"
                      width=40px
                      height=40px
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                    <input
                      class="flex-grow pl-8 pr-2 py-1 bg-gray-100 border rounded w-full"
                      :class="isDragging ? 'text-gray-600' : 'text-gray-900'"
                      :value="dateRange.end"
                      v-on="inputEvents.end"
                    />
                  </div>
                </div>
              </template>
            </v-date-picker>
          </div>
        </form>

        <!-- Buttons -->
        <div class="d-inline-flex">
          <div class="row">
            <span class="block text-gray-600 text-sm text-left font-weight-bold mb-2">Model</span>
            <div class="d-flex sm:flex-row justify-content-left">
              <br>
              <b-button-group>
                <b-button
                  v-for="(btn, idx) in modelButtons"
                  :key="idx"
                  :pressed.sync="btn.state"
                  variant="outline-success"
                  size="sm"
                  @click="onModelClick"
                >
                  {{ btn.caption }}
                </b-button>
              </b-button-group>
            </div>
          </div>
          <div class="row">
            <span class="block text-gray-600 text-sm text-left font-weight-bold mb-2">Transformations</span>
            <div class="d-flex sm:flex-row justify-content-left">
              <br>
              <b-button-group>
                <b-button
                  v-for="(btn, idx) in transformButtons"
                  :key="idx"
                  :pressed.sync="btn.state"
                  variant="outline-warning"
                  size="sm"
                  @click="onTransformClick"
                >
                  {{ btn.caption }}
                </b-button>
              </b-button-group>
            </div>
          </div>
          <div class="row">
            <span class="block text-gray-600 text-sm text-left font-weight-bold mb-2">Most Recent</span>
            <div class="d-flex sm:flex-row justify-content-left">
              <br>
              <b-button-group>
                <b-button
                  v-for="(btn, idx) in recentButtons"
                  :key="idx"
                  :pressed.sync="btn.state"
                  variant="outline-primary"
                  size="sm"
                  @click="onRecentClick"
                >
                  {{ btn.caption }}
                </b-button>
              </b-button-group>
            </div>
          </div>
        </div>
        <br><br>

        <!-- Main PLot -->

        <Plotly :data="datasets" :layout="layout" :display-mode-bar="true" @relayout="rePlot"></Plotly>
        <br><hr><br>

        <!-- Raw Data Table -->

        <h3>Raw Data</h3>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Date</th>
              <th scope="col">Open</th>
              <th scope="col">Low</th>
              <th scope="col">High</th>
              <th scope="col">Close</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in rawData.x" :key="index">
              <td>{{ index + 1 }}</td>
              <!-- <td>{{ new Date(row.Date).toISOString().substring(0, 10) }}</td> -->
              <td>{{ getMoment(row).format("YYYY-MM-DD") }}</td>
              <td >{{ rawData.y[index].Open }}</td>
              <td>{{ rawData.y[index].Low }}</td>
              <td>{{ rawData.y[index].High }}</td>
              <td>{{ rawData.y[index].Close }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment-timezone';
import { Plotly } from 'vue-plotly';
import { PlotData } from './helper/PlotData';

// Setup PlotData model state.
const pltData = new PlotData();

/* eslint-disable max-len */

export default {
  name: 'MainView',
  components: {
    Plotly,
  },
  data() {
    return {
      rawData: {},
      datasets: [{
        // Just some default values to show basic structure as an example.
        // x: [new Date('2020/01/02'), new Date('2020/01/03'), new Date('2020/01/06'), new Date('2020/01/07')],
        x: [1577923200000, 1578009600000, 1578268800000, 1578355200000],
        y: [10, 15, 13, 17],
        name: 'Initialization Data',
        type: 'line',
      }],
      layout: {
        title: 'Stock Price',
        // autosize: false,
        // width: 500,
        height: 650,
        // paper_bgcolor: '#7f7f7f',
        // plot_bgcolor: '#c7c7c7',
        // showlegend: true,
        legend: {
          x: 0,
          y: 1,
          xanchor: 'left',
        },
        xaxis: {
          autorange: true,
          type: 'date',
        },
        yaxis: {
          autorange: true,
        },
      },
      range: {
        start: '',
        end: '',
      },
      prevRange: {
        start: '',
        end: '',
      },
      masks: {
        input: 'YYYY-MM-DD',
      },
      modelButtons: [
        { caption: 'Raw', param: 'disable_raw', state: true },
        { caption: 'Linear Regression', param: 'linear', state: false },
        { caption: 'ARIMA', param: 'arima', state: false },
        { caption: 'Prophet', param: 'prophet', state: false },
      ],
      transformButtons: [
        { caption: 'Difference', param: 'diff', state: false },
        { caption: 'Log', param: 'log', state: false },
        { caption: 'Difference + Log', param: 'diff log', state: false },
      ],
      recentButtons: [
        { caption: 'Custom', state: true },
        { caption: '1 Month', state: false },
        { caption: '6 Months', state: false },
        { caption: '1 Year', state: false },
        { caption: '5 Year', state: false },
      ],
      otherdata: {},
    };
  },
  methods: {
    getData(force) {
      pltData.getData(this, force);
      // Re-scale the plot.
      this.layout.xaxis.autorange = true;
      this.layout.yaxis.autorange = true;
    },
    updateURL() {
      const qp = new URLSearchParams();

      // Update date range.
      qp.set('start_date', this.range.start);
      qp.set('end_date', this.range.end);

      // Update model patterns.
      this.modelButtons.forEach((btn) => {
        if (btn.param === 'disable_raw' && !btn.state) qp.set(btn.param, !btn.state);
        else if (btn.param === 'disable_raw' && btn.state) qp.delete(btn.param);
        else if (btn.state) qp.set(btn.param, btn.state);
      });

      // Update tranformation patterns.
      this.transformButtons.forEach((btn) => {
        if (btn.state) qp.set(btn.param, btn.state);
      });

      // Push the new URL to the history buffer.
      // eslint-disable-next-line
      history.pushState(null, null, `?${qp.toString()}`);
    },
    getLocalDateString(date) {
      return date
        .toLocaleDateString()
        .replace(/(\d{1,2})\/(\d{1,2})\/(\d{4})/g, '$3-$1-$2');
    },
    getISODateString(date) {
      return date
        .toISOString()
        .substring(0, 10);
    },
    getMoment(date) {
      return moment.tz(date, moment.tz.guess());
    },
    onModelClick() {
      this.getData(true);
      this.updateURL();
    },
    onTransformClick() {
      this.getData(true);
      this.updateURL();
    },
    onRecentClick() {
      this.dateRange = {
        start: '1982-01-18',
        end: '2000-1-1',
      };
    },
    rePlot(range) {
      const start = range['xaxis.range[0]'];
      const end = range['xaxis.range[1]'];
      if (start && start.length > 0 && end && end.length > 0) {
        this.dateRange = {
          start: start.substring(0, 10),
          end: end.substring(0, 10),
        };
      }
    },
  },
  computed: {
    dateRange: {
      set(val) {
        // Store previous date range so we can avoid unnecessary calls.
        this.prevRange = this.range;

        // Convert given value to date string.
        this.range = (val && (val.start instanceof Date)) ? {
          start: this.getISODateString(val.start),
          end: this.getISODateString(val.end),
        } : {
          start: val.start,
          end: val.end,
        };

        // Update data and URL GET parameters.
        this.getData();
        this.updateURL();
      },
      get() {
        const range = {
          start: this.range.start,
          end: this.range.end,
        };
        return range;
      },
    },
  },
  created() {
    // Check for current query parameters or set defaults.
    const start = this.$route.query.start_date;
    const end = this.$route.query.end_date;
    this.range = {
      start: (start && start.length > 0) ? start : '2020-01-01',
      end: (end && end.length > 0) ? end : '2022-04-01',
    };

    // Update buttons if any options are in query string.
    this.modelButtons.forEach((btn, i) => {
      if (this.$route.query.disable_raw) this.modelButtons[i].state = false;
      else if (this.$route.query[btn.param]) this.modelButtons[i].state = true;
    });
    this.transformButtons.forEach((btn, i) => {
      if (this.$route.query[btn.param]) this.transformButtons[i].state = true;
    });

    // Retrieve the resquested data from backend.
    this.getData();
    this.updateURL();
  },
};
</script>

<style>
.bg-grey {
  background: #f9f9f9;
}
</style>
