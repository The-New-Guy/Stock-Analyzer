import axios from 'axios';
import moment from 'moment-timezone';

/* eslint-disable max-len */
/* eslint-disable no-param-reassign */

class PlotData {
  client = axios.create({
    baseURL: 'http://localhost:5000/v1/client',
    timeout: 60000,
  });

  tz = moment.tz.guess();

  getData(comp, force) {
    // Get date range parameters.
    const startDate = typeof comp.range.start === 'string' ? comp.range.start : '2000-01-01';
    const endDate = typeof comp.range.end === 'string' ? comp.range.end : '2000-01-02';
    let path = `/data?start_date=${startDate}&end_date=${endDate}`;

    // Get model parameters.
    comp.modelButtons.forEach((btn) => {
      if (btn.param === 'disable_raw' && !btn.state) path = `${path}&disable_raw=true`;
      else if (btn.param !== 'disable_raw' && btn.state) path = `${path}&model=${btn.param}`;
    });

    // Get transform parameters.
    comp.transformButtons.forEach((btn) => {
      if (btn.state) path = `${path}&transform=${btn.param}`;
    });

    // Make the actual request if needed.
    if (
      comp.prevRange.start !== startDate
      || comp.prevRange.end !== endDate
      || force
    ) {
      this.client
        .get(path)
        .then((response) => {
          // Clear previous datasets.
          comp.datasets = [];

          // Set aside a copy of the raw data.
          if (!path.includes('disable_raw')) {
            [comp.rawData] = response.data.data;
          }

          // Build a list of plot datasets.
          // We also convert the timestamp to browser's local time.
          comp.datasets = response.data.data.map((row) => ({
            ...row,
            x: row.x.map((date) => (moment.tz(date, this.tz).valueOf())),
            y: row.y.map((col) => {
              if (col.Close) return col.Close; // TODO: Parameterize the field selected here.
              return col;
            }),
          }));
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  }
}

// eslint-disable-next-line import/prefer-default-export
export { PlotData };
