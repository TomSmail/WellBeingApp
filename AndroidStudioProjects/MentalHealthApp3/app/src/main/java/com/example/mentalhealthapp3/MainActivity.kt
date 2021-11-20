package com.example.mentalhealthapp3

import android.Manifest
import android.animation.ArgbEvaluator
import android.animation.ValueAnimator
import android.app.Activity
import android.content.pm.PackageManager
import android.graphics.Color
import android.media.MediaRecorder
import android.os.Bundle
import android.os.Environment
import android.util.Log
import android.view.WindowManager
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.graphics.ColorUtils
import java.io.IOException
import java.io.InputStream


class MainActivity : AppCompatActivity() {

    private var mediaRecorder: MediaRecorder? = null
    private var state: Boolean = false
    private val ACCESS_TOKEN: String = "sl.A6-mM6l6usTuFNoFuj5efa2pupKpvj3k12zSk9GWRwNzV372Y5iiJCvu1D2thKqmNPWZ1KfRcmn43OTYJOiVjqR5QUqUqJCCYcJhEfobEXfg68uuSzrDsjDjbO3EaOfOMw6hX0g"

    // I want to be able to click start recording again to stop the recording. Will make a boolean function to see if I am recording at the moment
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val buttonRecording = findViewById<Button>(R.id.buttonRecording)
        val output: String = Environment.getExternalStorageDirectory().absolutePath+"/recording.3gp"

        mediaRecorder?.setAudioSource(MediaRecorder.AudioSource.MIC)
        mediaRecorder?.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP)
        mediaRecorder?.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB)
        mediaRecorder?.setOutputFile(output)


        buttonRecording.setOnClickListener {

            if (ContextCompat.checkSelfPermission(this,
                    Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED && ContextCompat.checkSelfPermission(this,
                    Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                val permissions = arrayOf(
                    Manifest.permission.RECORD_AUDIO,
                    Manifest.permission.WRITE_EXTERNAL_STORAGE,
                    Manifest.permission.READ_EXTERNAL_STORAGE
                )
                ActivityCompat.requestPermissions(this, permissions, 0)
            }
            else if (ActivityCompat.checkSelfPermission(
                    this,
                    Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED && !state
            )
        {
                startRecording()
                Log.i("Starting Recording", "This is the start!")
            }
            else{
                stopRecording()
                Log.i("Output", "$output")
                Toast.makeText(this, "$output", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun startRecording() {
        try {
            mediaRecorder?.prepare()
            mediaRecorder?.start()
            state = true
            Toast.makeText(this, "Recording started!", Toast.LENGTH_SHORT).show()
        } catch (e: IllegalStateException) {
            e.printStackTrace()
        } catch (e: IOException) {
            e.printStackTrace()
        }
    }
    private fun stopRecording(){
        if(state){
            mediaRecorder?.stop()
            mediaRecorder?.release()
            state = false

        }else{
            Toast.makeText(this, "You are not recording right now!", Toast.LENGTH_SHORT).show()
        }
    }
    private fun moodRating(){

    }
    private fun saveRecording(filename: String, ){

    }
    suspend fun uploadFile(fileName: String, inputStream: InputStream): DropboxUploadApiResponse =
        withContext(Dispatchers.IO) {
            try {
                val fileMetadata = dropboxClient
                    .files()
                    .uploadBuilder("/$fileName") //Upload to the root of Dropbox
                    .withMode(WriteMode.OVERWRITE)
                    .uploadAndFinish(inputStream)
                DropboxUploadApiResponse.Success(fileMetadata)
            } catch (exception: DbxException) {
                DropboxUploadApiResponse.Failure(exception)
            }
        }

}
    /*override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if( requestCode == 111 && grantResults[0] == PackageManager.PERMISSION_GRANTED)


    }*/
}
