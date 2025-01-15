export interface User {
    id: number,
    username: string, 
    first_name: string, 
    last_name: string, 
    password: string, 
    profile_img_url : string,
    roles: string[]
}