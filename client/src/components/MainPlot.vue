<template>
  <div class="container">
    <div class="row">
      <div class="bg-grey col-sm-10">
        <h1>Stock Analyzer</h1>
        <hr><br><br>

        <!-- Date Range Picker -->

        <form class="shadow-md rounded px-8 pt-6 pb-8" @submit.prevent>
          <div class="mb-4">
            <!-- eslint-disable-next-line max-len -->
            <span class="block text-gray-600 text-sm text-left font-weight-bold mb-2">Select Range</span>
            <br>
            <v-date-picker
              v-model="range"
              mode="date"
              :masks="masks"
              is-range
              is-inline
              is-dark
              color="blue"
              @input="onRangeChange"
            >
              <template v-slot="{ inputValue, inputEvents, isDragging }">
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
                      <!-- eslint-disable-next-line max-len -->
                      <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                    <input
                      class="flex-grow pl-8 pr-2 py-1 bg-gray-100 border rounded w-full"
                      :class="isDragging ? 'text-gray-600' : 'text-gray-900'"
                      :value="inputValue.start"
                      v-on="inputEvents.start"
                      @change="emitEventChanged"
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
                      <!-- eslint-disable-next-line max-len -->
                      <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                    <input
                      class="flex-grow pl-8 pr-2 py-1 bg-gray-100 border rounded w-full"
                      :class="isDragging ? 'text-gray-600' : 'text-gray-900'"
                      :value="inputValue.end"
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
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-success btn-sm">Linear Regression</button>
                <button type="button" class="btn btn-success btn-sm">ARIMA</button>
                <button type="button" class="btn btn-success btn-sm">Prophet</button>
              </div>
            </div>
          </div>
          <div class="row">
            <!-- eslint-disable-next-line max-len -->
            <span class="block text-gray-600 text-sm text-left font-weight-bold mb-2">Transformations</span>
            <div class="d-flex sm:flex-row justify-content-left">
              <br>
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-warning btn-sm">Diff</button>
                <button type="button" class="btn btn-warning btn-sm">Log</button>
                <button type="button" class="btn btn-warning btn-sm">Diff + Log</button>
              </div>
            </div>
          </div>
        </div>
        <br><br>

        <!-- Main PLot -->

        <!-- eslint-disable-next-line max-len -->
        <Plotly v-model="plot" :data="data" :layout="layout" :display-mode-bar="true" @relayout="rePlot"></Plotly>
        <br><hr><br>
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
            <tr v-for="(row, index) in rawData" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ new Date(row.Date).toISOString().substring(0, 10) }}</td>
              <td>{{ row.Open }}</td>
              <td>{{ row.Low }}</td>
              <td>{{ row.High }}</td>
              <td>{{ row.Close }}</td>
            </tr>
          </tbody>
        </table>
        <br><hr><br>
        <h3>Debug</h3>
        Data : {{ this.data }}
        <br>
        Layout : {{ this.layout }}
        <br>
        Some Data : {{ this.somedata }}
        <br>
        Other Data : {{ this.otherdata }}
      </div>
    </div>
  </div>
</template>

<script>
import { Plotly } from 'vue-plotly';
import axios from 'axios';

export default {
  name: 'MainPlot',
  components: {
    Plotly,
  },
  data() {
    return {
      rawData: {},
      data: [{
        // Just some default values to show basic structure.
        x: [1, 2, 3, 4],
        y: [10, 15, 13, 17],
        type: 'line',
      }],
      layout: {
        title: 'Stock Price',
        xaxis: {
          type: 'date',
        },
      },
      range: {
        start: new Date(this.$route.query.start_date), // new Date(2020, 0, 1), // Jan. 1st 2020
        end: new Date(this.$route.query.end_date), // new Date(2022, 3, 1), // Apr. 1st 2022
      },
      inputValue: {},
      masks: {
        input: 'YYYY-MM-DD',
      },
      otherdata: {},
    };
  },
  methods: {
    getData() {
      const startDate = this.range.start.toISOString().substring(0, 10);
      const endDate = this.range.end.toISOString().substring(0, 10);
      const path = `http://localhost:5000/data?start_date=${startDate}&end_date=${endDate}`;

      axios
        .get(path)
        .then((response) => {
          // Parse response from JSON.
          this.rawData = JSON.parse(response.data.data);

          // TODO: Debug stuff; remove later.
          // this.otherdata = this.rawData.map((row) => new Date(row.Date).toLocaleDateString());
          // this.otherdata = new Date(this.otherdata.Date).toLocaleDateString();
          // this.otherdata = this.range;

          // Update compoment state with retrieved data.
          this.data = [{
            x: this.rawData.map((row) => new Date(row.Date)),
            y: this.rawData.map((row) => row.Close),
            type: 'line',
          }];
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onRangeChange(dateRange) {
      this.range = dateRange;
      this.getData();
      this.updateURL();
    },
    updateURL() {
      const qp = new URLSearchParams();
      qp.set('start_date', this.range.start.toISOString().substring(0, 10));
      qp.set('end_date', this.range.end.toISOString().substring(0, 10));
      // eslint-disable-next-line
      history.pushState(null, null, `?${qp.toString()}`);
    },
    rePlot(range) {
      this.otherdata = range;
      // eslint-disable-next-line
      this.range.start = new Date(range['xaxis.range[0]']);
      // eslint-disable-next-line
      this.range.end = new Date(range['xaxis.range[1]']);
      this.inputValue = {
        start: this.range.start,
        end: this.range.end,
      };
      this.getData();
      this.updateURL();
    },
  },
  computed: {
    somedata() {
      return 'hello';
    },
  },
  created() {
    // Check for current query parameters or set defaults.
    this.otherdata = 'here';
    const qp = new URLSearchParams(window.location.search);
    const start = qp.get('start_date');
    const end = qp.get('end_date');
    this.range.start = start ? new Date(start) : new Date('2020-01-01');
    this.range.end = end ? new Date(end) : new Date('2022-04-01');

    // Retrieve the resquested data from backend.
    this.getData();
    this.updateURL();
  },
  mounted() {
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
