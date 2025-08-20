class temp {
    long reverse(long x){
        long ret = 0;
        while(x != 0){
            ret = ret*10 + x%10;
            x/=10;
        }
        return ret;
    }
    boolean check(long x){
        long rev = reverse(x);
        int hash[] = new int[10];
        while(x!=0){
            if(x%10 != rev%10 || x%10==0 || rev%10 == 0){
                return false;
            }
            hash[(int)(x%10)]++;
            x/=10;
            rev/=10;
        }
        for(int i=1;i<=9;i++){
            if(hash[i] != 0 && hash[i] != i){
                return false;
            }
        }
        return true;
    }
    public long specialPalindrome(long n) {
        long top = (long)Math.pow(10,15);
        for(long i=n+1; i<=top; i++){
            if(check(i)){
                System.out.print(i+",");
            }
        }
        return -1;
    }

    public static void main(String args[]){
        temp obj = new temp();
        long result = obj.specialPalindrome(0);
    }
}