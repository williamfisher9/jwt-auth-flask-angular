import { Component, Input } from '@angular/core';
import { User } from '../interface/user';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [],
  templateUrl: './user-profile.component.html',
  styleUrl: './user-profile.component.css'
})

export class UserProfileComponent {

  @Input() user : User = null!;

  showFilePicker : boolean = false;

  selectedFile : File | null = null;

  showProfileImgPicker(){
    this.showFilePicker = true;
  }

  handleFileChange(event:any){
    this.selectedFile = event.target.files[0];
    console.log(this.selectedFile)
  }

  closeFilePicker(){
    this.showFilePicker = false;
  }

  uploadSelectedFile(){
    console.log(this.selectedFile)
  }

}
