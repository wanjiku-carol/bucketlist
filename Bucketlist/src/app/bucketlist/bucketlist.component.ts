import { Component, OnInit } from '@angular/core';
import { RestangularModule, Restangular } from 'ngx-restangular';
import { Router } from '@angular/router';
import { ModalModule } from 'ngx-bootstrap/modal';
import { ModalService } from '../_services/index';

@Component({
    selector: 'app-bucketlist',
    templateUrl: './bucketlist.component.html',
    styleUrls: ['./bucketlist.component.css'],
    moduleId: module.id,
})
export class BucketlistComponent implements OnInit{
    constructor(private restangular: Restangular,private router: Router,) {
    }
    bucketlists;
    name;
    // public reroute = false;
    getBuckelist(){
        let baseUrl = this.restangular.all('bucketlists');
        let getBucketlists = baseUrl.getList().subscribe(resp => {
            this.bucketlists = resp;
        });
    }
    deleteBucketlist(id){
        let baseUrl = this.restangular.one('bucketlists', id);
        let deleteBucketlists = baseUrl.remove().subscribe(resp=>{
            console.log(resp)
            window.location.reload();
        });
    }
    addBucketlist(){
        let baseUrl = this.restangular.all('bucketlists');
        let addBucketlists = baseUrl.post({'name':this.name});
        window.location.reload();
    }
    editBucketlist(id){
        let baseUrl = this.restangular.one('bucketlists', id);
        let addBucketlists = baseUrl.put({'name':this.name});
        window.location.reload();
    }

    logout() {
        localStorage.removeItem('auth_token');
        window.location.reload();
    }

    openModal(id: string){
        this.modalService.open(id);
    }


    // toItems(){
    //     this.reroute = true;
    //     // window.location.reload();
    // }

    ngOnInit() {
        this.getBuckelist();
    }

}
