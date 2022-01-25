<template>
    <div>
        <CAlert
                :show.sync="dismissCountDown"
                closeButton
                color="success"
                fade
                :show="alert_success"
        >
            User Information Created Successfully
        </CAlert>
        <CAlert closeButton :show.sync="dismissCountDown" show color="danger" :show="alert_danger">
            <strong>Error Occurred!</strong> When Creating User Information.
            <p>{{ error ? error.message : ""}}</p>
        </CAlert>
        <CRow>
            <CCol sm="24" md="12">
                <CCard>
                    <CCardHeader>
                        <h3> Class </h3>
                        <CButton color="success" @click="myModal = true" class="float-right mr-1">
                            Insert a new Class
                        </CButton>
                    </CCardHeader>
                    <CCardBody>
                        <CCol lg="12">
                            <CDataTable :items="Class" :fields=table_field
                                        striped
                                        fixed
                                        bordered
                            >
                                <template #show_details="{item, index}">
                                    <td class="py-2">
                                        <CButton
                                                color="success"
                                                square
                                                size="sm"
                                                @click="redirect_url(item, index)"
                                        >
                                            Details
                                        </CButton>
                                    </td>
                                </template>
                                <template #remove_details="{item, index}">
                                    <td class="py-2">
                                        <CButton
                                                color="danger"
                                                square
                                                size="sm"
                                                @click="redirect_url(item, index)"
                                        >
                                            Remove
                                        </CButton>
                                    </td>
                                </template>
                                <template #header>
                                    <CIcon name="cil-description"/> List of Class

                                </template>
                            </CDataTable>
                        </CCol>
                    </CCardBody>
                </CCard>
            </CCol>
        </CRow>
        <CModal
                title="Create a new Class"
                :show.sync="myModal"
                size="xl"
                :close-on-backdrop="false"
        >
            <CCol sm="24">
                <CCard>
                    <CCardHeader>
                        <strong>User Information</strong>
                    </CCardHeader>
                    <CCardBody>
                        <div>
                            <!-- <CRow>
                                <CCol md="12">
                                    <CInput
                                            key="proxy_provider_address"
                                            :was-validated="proxy_provider_address.was_validated"
                                            :is-valid="proxy_provider_address.was_validated"
                                            :description="proxy_provider_address.description"
                                            v-model="proxy_provider_address.value"
                                            label="User Address"
                                            placeholder="Enter User Address e.g. https://<proxy_provider_address>"
                                    />
                                </CCol>
                            </CRow>
                            <CInput
                                    key="time_interval"
                                    v-model="time_interval.value"
                                    label="Update Time Interval"
                                    placeholder="Enter Time Interval"
                                    type="number"
                                    min="10"
                                    :was-validated="time_interval.was_validated"
                                    :is-valid="time_interval.was_validated"
                                    :description="time_interval.description"

                            />
                            <CInputCheckbox
                                    v-model="is_https_filtered"
                                    label="Is Https Filtered"
                                    :value="true"
                                    :custom="key > 1"
                                    name="Is Https Filtered"
                            /> -->

                        </div>

                    </CCardBody>
                </CCard>
            </CCol>
            <template #footer>
                <CButton @click="myModal = false" color="danger">Discard</CButton>
                <CButton @click="submitProxyAddress()" color="success">Submit</CButton>
            </template>
        </CModal>
    </div>
</template>



<script>
    import CTableWrapper from '../base/Table.vue'
    window.axios = require('axios')
    export default {
        props: ['class_props'],
        name: 'Class',
        components: { CTableWrapper },
        mounted: function(){
            this.updateTableData();
        },
        data: function () {
            return {
                dismissCountDown: 5,
                show: true,
                alert_success: false,
                alert_danger: false,
                isCollapsed: true,
                Class: this.class_props,
                table_field: ["name", "unique_name", "is_archived", {
                    key: 'show_details',
                    label: '',
                    _style: 'width:1%',
                    sorter: false,
                    filter: false
                },
                {
                    key: 'remove_details',
                    label: '',
                    _style: 'width:1%',
                    sorter: false,
                    filter: false
                }
                ],
                name: {
                    value: null,
                    description: null,
                    was_validated: null,
                },

                unique_name: {
                    value: null,
                    description: null,
                    was_validated: null,
                },
                is_archived: false,
                success: null,
                error: null,
                myModal: false,

            }
        },
        methods: {
            countDownChanged (dismissCountDown) {
                this.dismiss = dismissCountDown
            },
            updateTableData: function(){
                const field = this
                const token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFkbWluQGdtYWlsLmNvbSIsInBhc3N3b3JkIjoicGJrZGYyX3NoYTI1NiQyNjAwMDAkS1l2Q2xBUWM3eTdxWFFqenRDSmhkRyRZc1NQckZnQnNLcWpIaFhybEtGTUlTclBQR3UxaEVYcU03NDJTRW1MRnpzPSIsImV4cCI6MTY0MzQ5MjA2Nn0.Mzgr5Wz9we71pdbktMbytpeZjEf-Fa9HqFYyAo9ckek'
                const config = {
                    headers: { Authorization: `Bearer ${token}` }
                };
                axios.get('http://localhost:8000/api/v1/class/',config).then(function(response){
                        field.Class = response.data.output
                        console.log(response.data.output)
                    }
                ).catch(error => this.Class = {
                    'error': 'Error Occurred'
                })
            },
            redirect_url: function (item, index) {
                console.log(index)
                console.log(item)
                this.$router.push({ path: `details/${item.id}`})
            },
            submitProxyRequest: function(){
                console.log('GOT')
                console.log(this.Class.value)
                console.log('GOT')
                this.Class.was_validated = false
                this.Class.description = 'Please provide a valid User address'


            },
            submitProxyAddress: function(){
                const fields = this
                fields.success = null
                fields.error = null

                fields.Class.is_superuser = true
                fields.Class.is_teacher = true

                fields.Class.is_student = true
                fields.Class.name = ''
                console.log(fields.is_https_filtered)
                axios.post('http://localhost:8000/api/proxy-service-provider/', {
                    data: {
                        proxy_provider_address: fields.proxy_provider_address.value,
                        time_interval: fields.time_interval.value,
                        is_https_filtered: fields.is_https_filtered === false || fields.is_https_filtered === null  ? false : true,

                    }
                }).then(function(response){
                    fields.success = response.data
                    fields.myModal = false
                    fields.alert_success = true;

                    fields.proxy_provider_address.was_validated = null
                    fields.time_interval.was_validated = null
                    fields.proxy_provider_address.description = ''
                    fields.proxy_provider_address.value = ''
                    fields.time_interval.description = ''
                    fields.time_interval.value = ''
                    fields.updateTableData();
                }).catch(function(error){
                    fields.error = error.response.data.message;
                    if(fields.error.hasOwnProperty('proxy_provider_address')){
                        fields.proxy_provider_address.was_validated = false
                        fields.proxy_provider_address.description = 'Please provide a valid User address'
                    }
                    if(fields.error.hasOwnProperty('time_interval')){
                        fields.time_interval.was_validated = false
                        fields.time_interval.description = 'Please provide a valid time_interval'
                    }
                })


            }

        }
    }
</script>
