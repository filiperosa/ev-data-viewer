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
                    <th>timestamp</th>
                    <th>speed</th>
                    <th>odometer</th>
                    <th>soc</th>
                    <th>elevation</th>
                    <th>shift_state</th>
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
    <Paginate
        :page-count="total_pages"
        :click-handler="changePage"
        :prev-text="'Prev'"
        :next-text="'Next'"
    />
</div>
</template>

<script>
export default {
    data() {
        return {
            API_URL: "/api/v1",

            //Filter variables
            selected_vehicle: "all",
            vehicles: [],
            from: null,
            to: null,

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
        // get vehicle datapoints from the API
        async getDatapoints(){
            let url = [`${this.API_URL}/vehicle_data`];

            console.log(this.selected_vehicle, this.from, this.to, this.selected_page, this.items_per_page);

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

            const rsp_full = await fetch(url.join(''));
            const response = await rsp_full.json();

            this.datapoints = response.items;
            this.total_pages = Math.floor(response.total/response.size);
            this.page = response.page;

            console.log(this.datapoints);
        },
        async getVehicleIds(){
            const rsp_full = await fetch(`${this.API_URL}/vehicles`);
            this.vehicles = await rsp_full.json();
        },
        // filter button click handler
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
        changePage(page){
            this.selected_page = page;
            console.log(`selected page: ${this.selected_page}`)
            this.getDatapoints();
        }
    },
    computed: {
        sortedDatapoints(){
            //TODO: sort datapoints here
            return datapoints
        },
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
    justify-content: center;
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
    height: 50vh !important;
    overflow: scroll;
}

thead {
    background-color: #343a40;
    color: white;
    position: sticky;
    top: 0;
}

/* thead::before {
    content:" ";
    display: block;
    position: absolute;
    top: -8px;
    height: 8px;
    width: 100%;
    background-color: solid white !important;
} */

thead:before{
    content:'';
    position:absolute;
    left: 0;
    top: -100px;
    width:100%;
    border-bottom: 100px solid white;
}

.pagination {
    justify-content: center;
    padding-top: 20px;
}

#vehicleIdInput {
    text-align: left;
}

.input-group {
    width: fit-content !important;
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