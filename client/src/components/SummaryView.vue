<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Summary</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Summarize</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Date</th>
              <th scope="col">Open</th>
              <th scope="col">Low</th>
              <th scope="col">High</th>
              <th scope="col">Close</th>
              <th scope="col">DailyIncrease</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in JSON.parse(summary)" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ new Date(row.Date).toLocaleDateString() }}</td>
              <td>{{ row.Open }}</td>
              <td>{{ row.Low }}</td>
              <td>{{ row.High }}</td>
              <td>{{ row.Close }}</td>
              <td>
                <span v-if="row.Open < row.Close">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      summary: {},
    };
  },
  methods: {
    getSummary() {
      let count;
      if ('count' in this.$route.query && !Number.isNaN(this.$route.query.count)) {
        count = this.$route.query.count;
      } else {
        count = 25;
      }
      const path = `http://localhost:5000/summary?count=${count}`;
      axios
        .get(path)
        .then((response) => {
          this.summary = response.data.summary;
          // this.summary = JSON.parse(this.summary);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getSummary();
  },
};
</script>
