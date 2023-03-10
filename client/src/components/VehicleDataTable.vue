<template>
<div id="vehicle-data-wrapper">
    <div class="header">
        <h2>Table of Vehicle Data</h2>
    </div>
    <div class="filters">
        <div class="input-group input-group-sm filter">
            <span class="input-group-text text-secondary bg-white">Vehicle ID</span>
            <select name="vehicleIdInput" id="vehicleIdInput" v-model="selected_vehicle" class="input-group-text text-secondary bg-white">
                <option value='all'>All</option>
                <option v-for="vehicle in vehicles" :value="vehicle.id" v-bind:key="vehicle.id">{{ vehicle.id }}</option>
            </select>
        </div>
        <div class="input-group input-group-sm filter">
            <span class="input-group-text text-secondary bg-white">From</span>
            <Datepicker v-model="from" model-type="yyyy-MM-dd HH:mm:ss.S" input-class-name="custom-datepicker"></Datepicker>
        </div>
        <div class="input-group input-group-sm filter">
            <span class="input-group-text text-secondary bg-white">To</span>
            <Datepicker v-model="to" show-now-button model-type="yyyy-MM-dd HH:mm:ss.S" input-class-name="custom-datepicker" ></Datepicker>
        </div>
        <button class="btn btn-primary" @click="filterButtonClick">Filter</button>
    </div>
    <div class="table-wrapper">
        <table id="vehicle-data-table" class="table table-hover">
            <thead class="thead-dark">
                <tr>
                    <th @click="sort">Timestamp</th>
                    <th>Speed</th>
                    <th>Odometer</th>
                    <th>Soc</th>
                    <th>Elevation</th>
                    <th>Shift state</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="datapoint in datapoints" v-bind:key="datapoint.id">
                    <td>{{ datapoint.timestamp }}</td>
                    <td>{{ datapoint.speed }}</td>
                    <td>{{ datapoint.odometer }}</td>
                    <td>{{ datapoint.state_of_charge }}</td>
                    <td>{{ datapoint.elevation }}</td>
                    <td>{{ datapoint.shift_state ? datapoint.shift_state.id : ''}}</td>
                </tr>
            </tbody>
        </table>
    </div>
    <nav>
        <Paginate
            :page-count="total_pages"
            :click-handler="changePage"
            :prev-text="'Prev'"
            :next-text="'Next'"
        />
        <div class="input-group input-group-sm">
            <span class="input-group-text text-secondary bg-white">Per page:</span>
            <select class="form-select" aria-label="Select items per page" v-model="items_per_page" @change="getDatapoints" >
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="20">20</option>
                <option value="50">50</option>
                <option value="100">100</option>
            </select>                               
        </div>
    </nav>
    <div class="graph-section">
        <div class="graph-box">
            <line-chart :datasets="[speedData, socData, elevationData]" />
        </div>
        <div class="graph-box-small">
            <line-chart :datasets="[odometerData]" />
        </div>
        <div class="graph-box-small">
            <pie-chart :labels="gearStats.labels" :data="gearStats.data" />
        </div>
    </div>
</div>
</template>

<script>
import LineChart from './LineChart.vue';
import PieChart from './PieChart.vue';
export default {
    components: { LineChart, PieChart },
    data() {
        return {
            API_URL: "/api/v1",

            //Filter variables
            selected_vehicle: "all",
            vehicles: [],
            from: null,
            to: null,
            order_asc: true,

            // Data to display
            datapoints: [{"id":451,"speed":200,"state_of_charge":50,"shift_state_id":"D","vehicle_id":"123","timestamp":"2023-01-19T14:25:12.336794","odometer":49923.2,"elevation":130,"shift_state":{"id":"D","name":"Drive"}}],
            
            //Pagination variables
            selected_page: 1,
            items_per_page: 50,
            total_pages: 10
        };
    },
    methods: {
        updateDatapoints(){
            //TODO: call the API
            return
        },
        //
        // Get vehicle datapoints from the API
        async getDatapoints(){
            let url = [`${this.API_URL}/vehicle_data`];

            // build the url with all the filtering options
            //
            if(this.selected_vehicle != 'all'){
                url.push(`/${this.selected_vehicle}`)
            }
            url.push('?');
            if(this.from){
                url.push(`from_date=${this.from}&`);
            }
            if(this.to){
                url.push(`to_date=${this.to}&`);
            }
            url.push(`page=${this.selected_page}&`);
            url.push(`size=${this.items_per_page}&`);
            url.push(`order=${this.order_asc ? 'asc' : 'desc'}`);

            // fetch the data
            const rsp_full = await fetch(url.join(''));
            const response = await rsp_full.json();

            // unpack the data
            this.datapoints = response.items;
            this.total_pages = Math.floor(response.total/response.size);
            this.page = response.page;

            console.log(this.datapoints);
        },
        //
        // Get all the vehicle ids from the API
        async getVehicleIds(){
            const rsp_full = await fetch(`${this.API_URL}/vehicles`);
            this.vehicles = await rsp_full.json();
        },
        //
        // Filter button click handler
        filterButtonClick() {
            this.selected_page = 1;
            console.log(`Search datapoints from ${this.from} to ${this.to}`);
            if (this.from > this.to) {
                alert("From date must be before To date");
                this.to = null;
                this.from = null;
                return;
            }

            this.getDatapoints();
        },
        //
        // Handle page change
        changePage(page){
            this.selected_page = page;
            console.log(`selected page: ${this.selected_page}`)
            this.getDatapoints();
        },
        //
        // Invert sorting order by timestamp
        sort(){
            this.order_asc = !this.order_asc;
            console.log(this.order_asc)
            this.getDatapoints();
        }
    },
    computed: {
        gearStats() {
            let gears = {}
            for (let d of this.datapoints) {
                const shift_name = d.shift_state ? d.shift_state.name : 'None';

                if (gears[shift_name]) {
                    gears[shift_name] += 1;
                } else {
                    gears[shift_name] = 1;
                }         
            }

            return {
                labels: Object.keys(gears),
                data: Object.values(gears)
            }
        },
        speedData() {
            let data = []
            for (let d of this.datapoints) {
                if (d.speed) {
                    data.push({x: d.timestamp, y: d.speed});
                }
            }
            return {
                label: 'Speed',
                data: data,
                backgroundColor : '#f87979',
                borderColor : '#f8797980',
                tension: 0.1
            }
        },
        socData() {
            let data = []
            for (let d of this.datapoints) {
                if (d.state_of_charge) {
                    data.push({x: d.timestamp, y: d.state_of_charge});
                }
            }
            return {
                label: 'Soc',
                data: data,
                backgroundColor: '#41B883',
                borderColor: '#41B88380',
            }
        },
        odometerData() {
            let data = []
            for (let d of this.datapoints) {
                if (d.odometer) {
                    data.push({x: d.timestamp, y: d.odometer});
                }
            }
            return {
                label: 'Odometer',
                data: data,
                backgroundColor: '#ffbb00',
                borderColor: '#ffbb0080',
            }
        },
        elevationData() {
            let data = []
            for (let d of this.datapoints) {
                if (d.elevation) {
                    data.push({x: d.timestamp, y: d.elevation});
                }
            }
            return {
                label: 'Elevation',
                data: data,
                backgroundColor: '#007bff',
                borderColor: '#007bff80',
            }
        }
    },
    mounted() {
        //TODO: load data from API (pre-fill vehicle id dropdown)
        this.getDatapoints();
        this.getVehicleIds();
    }
};
</script>

<style scoped>

.filters {
    display: flex;
    justify-content: space-between;
    align-content: center;
    flex-direction: row;
    flex-wrap: nowrap;
    align-items: center;

    padding-top: 20px;
    padding-bottom: 20px;

    border-bottom: 1px solid black;
    border-top: 1px solid black;
}

.filters > .filter {
    margin-right: 15px;
}

.table-wrapper {
    padding-top: 20px;
    max-height: 50vh !important;
    overflow: scroll;
}

thead {
    background-color: #343a40;
    color: white;
    position: sticky;
    top: 0;
}

thead:before{
    content:'';
    position:absolute;
    left: 0;
    top: -100px;
    width:100%;
    border-bottom: 100px solid white;
}

thead th:first-child {
    cursor: pointer;
}

#vehicleIdInput {
    text-align: left;
}

.input-group {
    width: fit-content !important;
}

nav {
    display: flex;
    justify-content: center;
    padding-top: 20px;
}

nav > .input-group {
    height: 38px;
    margin-left: 1rem;
}

.graph-section {
    height: 30vh;
    display: flex;
    justify-content: space-between;
    align-content: center;
    flex-direction: row;
    flex-wrap: nowrap;
    align-items: center;
}

.graph-box {
    width: 50%;
    height: 100%;
}

.graph-box-small {
    width: 25%;
    height: 100%;
}

/* Persisten scrollbar  */

::-webkit-scrollbar {
  -webkit-appearance: none;
  width: 7px;
}

::-webkit-scrollbar-thumb {
  border-radius: 4px;
  background-color: rgba(0, 0, 0, .5);
  box-shadow: 0 0 1px rgba(255, 255, 255, .5);
}
</style>

<style>
.custom-datepicker {
    height: 31px !important;
    width: 200px !important;
    border-top-left-radius: 0 !important;
    border-bottom-left-radius: 0 !important;
}
</style>