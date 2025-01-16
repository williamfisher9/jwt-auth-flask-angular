import { Component, Input } from '@angular/core';
import { User } from '../interface/user';
import { AppService } from '../services/app.service';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [],
  templateUrl: './user-profile.component.html',
  styleUrl: './user-profile.component.css'
})

export class UserProfileComponent {

  constructor(private appService : AppService){}

  @Input() user : User = null!;

  showFilePicker : boolean = false;

  selectedFile : File | null = null;
  selectedFileUrl : string = '';

  isLoading : boolean = false;

  errorMessage : string = ''

  showProfileImgPicker(){
    this.showFilePicker = true;
  }

  handleFileChange(event:any){
    this.selectedFile = event.target.files[0];
    this.selectedFileUrl = window.URL.createObjectURL(event.target.files[0])
    this.errorMessage = "";
  }

  closeFilePicker(){
    this.showFilePicker = false;
    this.selectedFileUrl = '';
    this.selectedFile = null;
  }

  uploadSelectedFile(){
    this.errorMessage = '';
    this.isLoading = true;
    if(this.selectedFile != null){
      this.appService.updateProfileImage(this.user.id, this.selectedFile).subscribe({
        next: (res) => {
          this.user.profile_img_name = res.message;
        },
        error: (err) => {
          this.isLoading = false;
          this.errorMessage = err.error.message;
        },
        complete: () => {
          this.isLoading = false;
          this.showFilePicker = false;
          this.selectedFile = null;
          this.selectedFileUrl = '';
        }
      })
    } else {
      this.errorMessage = "Pick an image first";
      this.isLoading = false;
    }
      
  }

}
